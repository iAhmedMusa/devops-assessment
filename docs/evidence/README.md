# Evidence

Screenshots, scan output, and plan output from real runs — no mocked or
synthetic output. Grouped by capability, not by task number. The 3
screenshots embedded in the root [README](../../README.md)'s Evidence
section are a subset of what's here.

---

## Orchestration — pods actually running

**Local cluster, all three services:**

Two backend replicas, two frontend replicas, one postgres — all running
in the `plinth-local` namespace:

![kubectl get all — local namespace](Screenshot%202026-07-04%20at%2011.07.11.png)

**Production namespace (multi-replica):**

Three backend replicas, two frontend replicas, one postgres — all
`Running`, all `1/1 Ready`:

![kubectl get all — production namespace](Screenshot%202026-07-04%20at%2011.05.50.png)

Both confirm the manifests work as declared: 2+ replicas, readiness
probes passing, services are `ClusterIP` (no external IPs), and the
database runs as `postgres  5432/TCP  <none>` — never exposed
externally. See [`docs/networking.md`](../networking.md) for why.

---

## Release pipeline — real, end to end

**Full pipeline success (v0.1.2):** all 7 jobs passed — test backend,
test frontend, build and push images, mock ECR push, GitHub release,
mock staging deploy, mock production deploy. Total: 14m 19s.

![Pipeline v0.1.2 — all jobs green](Screenshot%202026-07-04%20at%2011.28.47.png)

**Build artifacts:** frontend build record (112 KB), backend build
record (95.8 KB), Trivy scan results (8.15 KB) — three artifacts from
one run.

![Artifacts — build records + Trivy scan](Screenshot%202026-07-04%20at%2011.28.59.png)

**Build details:** frontend build 8m 21s, backend build 2m 21s, both
0% cache (clean builds).

![Build summary — frontend and backend](Screenshot%202026-07-04%20at%2011.29.09.png)

**Staging deploy in progress (v0.2.0):** the "Deploy to staging (kind)"
job actually running — proves the real kind-cluster deploy step works,
not just that it's mocked elsewhere in the graph.

![Staging deploy running](Screenshot%202026-07-04%20at%2011.57.54.png)

**Production approval gate (v0.2.1):** pipeline paused at "Deploy to
production" — the `production` GitHub environment's protection rule
requesting a review before the job proceeds.

![Waiting for production review](Screenshot%202026-07-04%20at%2012.17.34.png)

**Approval dialog:** the "Review pending deployments" modal — a
reviewer must check the `production` environment and click "Approve
and deploy."

![Approval dialog](Screenshot%202026-07-04%20at%2012.17.43.png)

**Pipeline success after approval (v0.2.1):** all 7 jobs green after
manual approval, 16m 30s total. The full chain — test → build →
release → staging → approval → production — completed end to end.

![Pipeline success after approval](Screenshot%202026-07-04%20at%2012.17.54.png)

**Latest pipeline run (v0.3.0):** triggered by the `feat/terraform-eks`
merge, all jobs passed, 14m 57s.

![Pipeline v0.3.0 — all jobs green](Screenshot%202026-07-04%20at%2013.11.00.png)

Live links: [Actions run 28698340896](https://github.com/iAhmedMusa/plinth/actions/runs/28698340896) (v0.3.0), [release v0.3.0](https://github.com/iAhmedMusa/plinth/releases/tag/v0.3.0).

---

## Supply-chain security — real Trivy scan output

The screenshot above shows the scan *ran*; this is what it actually
found, pulled from the real artifact of the v0.1.2 run
([`trivy-backend.txt`](trivy-backend.txt), [`trivy-frontend.txt`](trivy-frontend.txt) — full raw output, not excerpted). Aggregate counts below are copied directly from each file's own `Total:` lines, not hand-tallied:

**Backend** (`ahmedmusa/devops-assessment-backend:1ac1492`):

| Layer | Total | High | Critical |
|---|---|---|---|
| OS packages (debian 13.5) | 11 | 9 | 2 |
| Python packages | 3 | 3 | 0 |

Two findings with an unambiguous single-row severity in the raw table:
`CVE-2026-42496` (perl-base, **CRITICAL**, fix deferred — path traversal
via crafted tar archive) and `CVE-2026-41992` (gzip, **HIGH** — global
buffer overflow). The rest of the breakdown is in the raw file; several
rows use Trivy's merged-cell rendering for repeated values, which isn't
worth mis-transcribing here.

**Frontend** (`ahmedmusa/devops-assessment-frontend:1ac1492`):

| Layer | Total | High | Critical |
|---|---|---|---|
| OS packages (alpine 3.23.4) | 2 | 2 | 0 |
| Node.js packages | 21 | 21 | 0 |

The one clearly single-row OS finding: `CVE-2026-45447` (libcrypto3/
libssl3, **HIGH** — OpenSSL heap use-after-free in `PKCS7_verify()`,
fixed in 3.5.7-r0). The 21 Node.js findings span several transitive
dependencies (`next`, `cross-spawn`, `glob`, `minimatch`, `sigstore`,
`tar`) — see the raw file for the per-package breakdown.

Both scans ran with `exit-code: "0"` — report-only, as documented in
[ADR-0006](../decisions/0006-multi-arch-images-and-trivy-gate.md). None
of the above blocked the release; that's a disclosed limitation, not an
oversight. The `scan-terraform` job added later in `deploy.yml` covers
IaC misconfigurations the same way.

---

## Infrastructure as code — a real Terraform plan

Full plan output: [`tfplan-dev.txt`](tfplan-dev.txt). Commands run to
produce it:

```bash
cd terraform
terraform init -backend=false
terraform validate                              # passes
terraform fmt -check -recursive                  # passes
terraform plan -var-file=envs/dev.tfvars \
  -out=tfplan-dev 2>&1 | tee tfplan-dev.txt
```

| Module | Resources | What it creates |
|--------|-----------|-----------------|
| `network` | 19 | VPC, 3 public subnets, 3 private-app subnets, 3 private-db subnets, IGW, NAT, route tables, associations |
| `eks` | 14 | EKS cluster (v1.30), managed node group (t3.medium, 2 nodes), OIDC provider, IAM roles, security groups |
| `ecr` | 4 | Two ECR repos (backend + frontend) with lifecycle policies, immutable tags, scan-on-push |
| `rds` | 3 | PostgreSQL 16 instance, subnet group, security group (SG-to-SG ingress from nodes) |
| `monitoring` | 5 | CloudWatch log groups, Container Insights addon, CPU alarm, storage alarm, SNS topic |

**Total: 59 resources to create, 0 to change, 0 to destroy** — run with
placeholder credentials (`AWS_ACCESS_KEY_ID=test`), no real AWS account
reachable. See `terraform/README.md` section 9 for why a fully
credential-free plan is possible at all.

Notable from the plan:

- **Three-tier VPC**: public subnets (IGW route), private-app subnets
  (NAT route), private-db subnets (no default route — no path out)
- **EKS cluster**: Kubernetes 1.30, API/audit/authenticator logging,
  public endpoint restricted to `0.0.0.0/0` (dev), `prevent_destroy` set
- **Node group**: `t3.medium`, desired 2 / min 1 / max 2,
  `create_before_destroy`, `ignore_changes` on desired_size
- **ECR repos**: `IMMUTABLE` tag mutability, AES256 encryption,
  scan-on-push enabled, lifecycle keeps last 20 tagged images, expires
  untagged after 7 days
- **RDS**: PostgreSQL 16, `publicly_accessible = false`,
  `manage_master_user_password = true` (password in Secrets Manager,
  never in Terraform), `deletion_protection = true`,
  `prevent_destroy = true`, gp3 storage with autoscaling to 100 GB
- **Monitoring**: CloudWatch log groups with 30-day retention, Container
  Insights addon, node CPU alarm (>80% for 10 min), RDS storage alarm
  (<2 GB free)

---

## What's not here yet

No screenshot of the running UI in a browser — everything above proves
the pods and pipeline, not what a user would actually see at
`localhost:3000`. Adding one is a `docker compose up -d --build` and a
screenshot away; it just hasn't been captured yet.
