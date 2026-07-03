# Kubernetes manifests (Kustomize)

Traffic flows `ingress-nginx -> frontend (Next.js) -> backend (FastAPI,
internal-only) -> postgres`. Locally postgres runs in-cluster as a dev
stand-in with an ephemeral `emptyDir`; staging/production point the backend
at a managed cloud database instead (see the Terraform/database docs phase)
-- `k8s/base/postgres.yaml` is never applied there.

## Local run

1. Install ingress-nginx (Docker Desktop Kubernetes / kind):

       kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.2/deploy/static/provider/cloud/deploy.yaml

2. Deploy:

       kubectl apply -k k8s/overlays/local

3. Check pods:

       kubectl get pods -n devops-assessment-local

4. Open http://devops.localtest.me (resolves to 127.0.0.1 via public DNS,
   no `/etc/hosts` edit needed).

## Image tags

Base manifests reference `PLACEHOLDER/devops-assessment-{backend,frontend}:0.0.0`
-- never built or pulled directly. Each overlay's `images:` transformer
rewrites this to the real Docker Hub repository and a pinned semver tag
(`local`/`staging` currently pinned to `0.1.0` as an example; `production`
likewise, plus a replica-count patch). CI updates the tag in the relevant
overlay during deploy (next phase). `latest` is never used anywhere in this
repo.

## Requirements mapping

| Requirement                          | Where satisfied                                    |
|---------------------------------------|-----------------------------------------------------|
| 2 replicas (frontend & backend)       | `base/frontend-deployment.yaml`, `base/backend-deployment.yaml` |
| Readiness/liveness probes             | same two files (`/health` for backend, `/` for frontend) |
| Resource requests/limits              | same two files                                       |
| Non-secret config via ConfigMap       | `base/backend-configmap.yaml`                        |
| Secret example (no real values)       | `base/backend-secret-example.yaml`                   |
| Backend internal-only (ClusterIP)     | `base/backend-service.yaml`                          |
| Ingress routes to frontend only       | `base/ingress.yaml`                                  |
| Pod hardening (non-root, no priv esc, drop caps, read-only rootfs) | `base/backend-deployment.yaml`, `base/frontend-deployment.yaml` |
| Network isolation                     | `base/network-policies.yaml`                         |
| Disruption budgets                    | `base/pdb.yaml`                                      |
| No `latest` tags                      | `images:` transformers in every overlay              |
| Per-environment namespaces/images     | `overlays/{local,staging,production}/kustomization.yaml` |

## The "backend" Service-name constraint

The frontend's Next.js `/api/*` rewrite target (`http://backend:8080`) is
baked into the image at build time -- see the root
[README](../README.md#architecture) design decisions. `base/backend-service.yaml`
must keep the name `backend` exactly; renaming it silently breaks the
frontend-to-backend proxy without a frontend rebuild.

## Verification run

    kubectl apply -k k8s/overlays/local --dry-run=client
