# CI/CD pipeline

Workflow file: [`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml)

## 1. Pipeline overview

```mermaid
flowchart LR
    subgraph "PR path (pull_request)"
        A1[test-backend] --> A2[quality gate]
        A3[test-frontend] --> A2
    end

    subgraph "Tag path (push v*.*.*)"
        B1[test-backend] --> B3[build-and-push]
        B2[test-frontend] --> B3
        B3 --> B4["[MOCK] mock-ecr-push"]
        B3 --> B5[release]
        B5 --> B6["[MOCK] deploy"]
    end
```

Opening a pull request runs the two test jobs only — nothing is built,
pushed, or released. Pushing a `v*.*.*` tag runs the full chain: tests gate
the build, the build gates both the mock ECR push and the GitHub release,
and the release gates the mock deploy.

## 2. Trigger model

| Event                        | What runs                                    |
|-------------------------------|-----------------------------------------------|
| `pull_request`                | `test-backend`, `test-frontend`               |
| `push` of tag `v*.*.*`        | full pipeline (test → build/push → release/mock-ecr → mock deploy) |

To cut a release:

```
git tag v1.0.0
git push origin v1.0.0
```

Ordinary commits and PRs never trigger a build or a release — only an
explicit version tag does. This keeps `main` cheap to push to while making
every published image traceable to one tag.

## 3. Image tagging policy

Every image is tagged twice:

- **semver**, from the tag itself (`v1.0.0` → `1.0.0`)
- **immutable short SHA** (`git rev-parse --short HEAD`)

`latest` is never used. A floating tag can silently change under a
deployment that references it, which defeats reproducibility and makes
rollbacks ambiguous — pin to a semver or a SHA and both point at exactly one
image, forever.

## 4. Registry strategy

Docker Hub is used as the real registry: images are actually built and
pushed there on every tag, using a free-tier account, so the pipeline is
provable end-to-end rather than described. The assessment's own wording
("push images to ACR or ECR, or mock the push") is satisfied by an ECR push
step that is clearly labeled `[MOCK]` and only echoes the exact command
sequence a real push would run — it never calls the AWS API.

The mock step's comments describe the intended production path: no AWS
access keys in the repo at all, only GitHub OIDC federation
(`aws-actions/configure-aws-credentials` with `role-to-assume`), which
exchanges a short-lived token for the run rather than storing a long-lived
credential.

## 5. Secrets management

**What lives in GitHub Secrets today:**

- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` — a scoped Docker Hub access
  token, not the account password. It can be revoked and rotated
  independently of the account credential, and it only grants push access
  to this repo's images.

**How production would differ:**

- Cloud authentication (AWS/Azure) would use OIDC federation instead of
  long-lived keys — the workflow requests a short-lived token from the
  cloud provider's STS at run time, and nothing cloud-related is stored as
  a GitHub secret.
- Application runtime secrets (database credentials, API keys the running
  service needs) belong in a managed secret store — AWS Secrets Manager or
  Azure Key Vault — injected at deploy time, not baked into images or
  checked into the workflow.
- Production deploys would run under a GitHub environment with required
  reviewers, so a human approves the gate between "image built" and
  "image running in production."

**What must never be in the repo:** `.env` files, kubeconfig, cloud access
keys, or Terraform state. All of these are excluded via `.gitignore` and
must stay that way even as the pipeline grows.
