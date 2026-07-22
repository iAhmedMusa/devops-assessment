# Repo Audit

Read-only survey ahead of the Plinth restructuring. No files were edited to produce this — findings only.

---

## 1. Assessment/task framing to rewrite

| File | Line(s) | Current wording | Suggested replacement |
|---|---|---|---|
| `README.md` | 1 | `# DevOps Assessment` | `# Plinth` |
| `README.md` | 23 | `## What was built (task by task)` | delete section header; replace with capability matrix |
| `README.md` | 25 | `### Task 1 — The app` | fold into "Repository map" / capability matrix, no task numbering |
| `README.md` | 29 | `### Task 2 — CI/CD pipeline` | same — becomes a capability row linking `docs/ci-cd.md` |
| `README.md` | 33 | `### Task 3 — Kubernetes manifests` | same — links `k8s/README.md` |
| `README.md` | 37 | `### Task 4 — Private database connectivity` | same — links `docs/networking.md` |
| `README.md` | 41 | `### Task 5 — Infrastructure as code (Terraform)` | same — links `terraform/README.md` |
| `README.md` | 45 | `### Task 6 — Troubleshooting` | same — links `docs/operations/runbook.md` |
| `README.md` | 49 | `### Task 7 — Future improvements` | same — links `docs/roadmap.md` |
| `docs/proof.md` | 3 | "Evidence for each task, grouped by requirement." | "Evidence, grouped by capability." |
| `docs/proof.md` | 8, 26, 89, 97, 101, 109, 158, 165 | `## Task N — ...` headers | reframe as capability names (Application, Pipeline, Manifests, Networking, IaC, Runbook, Roadmap) |
| `k8s/README.md` | 30 | `## Requirements mapping` / `| Requirement | Where satisfied |` | `## Capability mapping` / `| Capability | Where satisfied |` |
| `docs/ci-cd.md` | 82 | `The assessment's own wording ("push images to ACR or ECR, or mock the push")` | "The original constraint ('push images to ACR or ECR, or mock the push')" |
| `terraform/README.md` | 42, 149 | "for this assessment to point at" / "out of scope for an assessment that will never be..." | "for this platform to point at" / "out of scope for a repo with no live backend" |
| `terraform/README.md` | (rationale prose) | multiple "this assessment" cost-tradeoff notes | "this reference deployment" / "this environment" |
| `terraform/provider.tf` | 26 | comment referencing "assessment" | reword to "reference deployment" |
| `terraform/backend.tf` | 12, 17-18 | "a real deployment this assessment explicitly does not make" | "a real deployment this repo intentionally stops short of" |
| `terraform/modules/network/README.md` | 36, 41 | "this assessment" (cost tradeoff framing) | "this reference deployment" |
| `terraform/modules/network/variables.tf` | 18 | "cost-optimized (this assessment)" | "cost-optimized (single-NAT default)" |
| `terraform/modules/network/main.tf` | 5, 98 | "requirement for this assessment" / "deliberate cost choice for this assessment" | "deliberate cost/HA tradeoff, see ADR-000x" |
| `terraform/modules/eks/main.tf` | 27 | "a bastion/VPN for the assessment" | "a bastion/VPN here" |
| `terraform/modules/eks/README.md` | 45 | "reachable for this assessment without standing up a..." | "reachable here without standing up a..." |
| `terraform/modules/rds/README.md` | 65 | "assessment — a Multi-AZ standby roughly doubles..." | "here — a Multi-AZ standby roughly doubles..." |
| `terraform/modules/rds/main.tf` | 63 | "THE core requirement for this database" | "THE core constraint for this database" |
| `terraform/modules/rds/variables.tf` | 38 | "cost trade-off for this assessment" | "cost tradeoff for this reference deployment" |
| `k8s/base/network-policies.yaml` | 3-4 | "satisfy the assessment's ingress-isolation requirement" | "satisfy the default-deny ingress posture (ADR-0005)" |
| `k8s/base/backend-service.yaml` | 13 | "internal-only per assessment" | "internal-only by design" |
| `docs/database-connectivity.md` | 66 | "hardening step beyond this assessment's scope" | "hardening step out of scope here" |

Every other `assessment` hit in `docs/proof/tfplan-dev.txt` is Terraform resource-name output (`devops-assessment-dev-*`), not prose — covered in section 2, not this one.

---

## 2. `devops-assessment` occurrences, by risk

**Safe to rename** (prose, docs, non-live identifiers):
- `README.md`, `frontend/README.md`, `backend/README.md` — monorepo name references
- `docs/troubleshooting.md`, `docs/future-improvements.md`, `docs/database-connectivity.md`, `docs/proof.md`, `terraform/README.md`, `terraform/modules/**/README.md` — prose mentions
- `terraform/modules/network/variables.tf:2` — description text only, not a default value

**Needs care** (functional identifiers — must be renamed consistently across every reference, and re-verified with `docker compose config`, `kubectl kustomize`, `terraform validate` after):
- `docker-compose.yml:1` — `name: devops-assessment` (compose project name)
- `terraform/variables.tf:20`, `terraform/terraform.tfvars.example:8,22`, `terraform/envs/{dev,staging,production}.tfvars` — `cluster_name` / `Project` tag defaults
- `k8s/base/**` — `namespace` labels, `app.kubernetes.io/part-of`, ingress host/name (`k8s/base/ingress.yaml`), image refs (`PLACEHOLDER/devops-assessment-{backend,frontend}`)
- `k8s/overlays/{local,staging,production,ci}/kustomization.yaml` and `namespace.yaml` — namespace names (`devops-assessment-local` etc.), `newName` image rewrites
- `.github/workflows/deploy.yml` — Docker Hub image names (`devops-assessment-backend/frontend`), kind cluster name (`devops-assessment-ci`), the commented future ECR path
- `docs/proof/tfplan-dev.txt` — plan output full of `devops-assessment-dev-*` resource/tag names — this is a **captured artifact**, not live code; regenerate a fresh `terraform plan` under the new naming rather than hand-edit it

**Do-not-touch (confirmed no live resources exist — see below, so this list is precautionary rather than active)**:
- `terraform/backend.tf:17-18` — commented-out example `bucket`/`key` values are illustrative only, never applied
- No `terraform apply` has been run against real AWS for any env — `terraform/README.md` and `docs/proof/tfplan-dev.txt` both confirm the evidence captured is `terraform plan` output only ("credential-free plan" per `terraform/README.md:235`). **There is no live infrastructure**, so cluster/tag/state-key renames carry no destroy/recreate risk. Recommend still doing the rename in its own session (Session 2) with a fresh `terraform validate`/`plan` per env as verification, and calling this out explicitly in an ADR rather than assuming.

---

## 3. Redaction check

No AWS account IDs, access keys, or real ARNs found. Specifics:
- All `arn:aws:iam::aws:policy/...` hits are AWS-owned managed-policy ARNs (public, not account-specific) — safe as-is.
- `.github/workflows/deploy.yml:175` — `arn:aws:iam::<aws-account-id>:role/gha-ecr-push` is already an explicit placeholder — safe.
- `docs/database-connectivity.md:73` — RDS hostname is already redacted (`devops-assessment-production-db.xxxx.ap-southeast-1.rds.amazonaws.com`) — safe, just needs the name-prefix rename in section 2.
- CIDR blocks present (`10.0.0.0/16`, `10.1.0.0/16`, `10.2.0.0/16`, `0.0.0.0/0`) are all non-sensitive, intentional example ranges — no redaction needed.
- `k8s/README.md:24`, `k8s/base/ingress.yaml:10`, `.github/workflows/deploy.yml:263` — `devops.localtest.me` / `127.0.0.1` is a public wildcard-DNS test domain, not a real host — safe, only needs the `devops` prefix considered for rename to `plinth.localtest.me` for consistency.
- `docs/proof/*.png` — not machine-readable by this pass; **manually eyeball each screenshot before publishing** for any AWS console chrome showing an account ID/ARN in the URL bar or account switcher. Flagging as an open item for the evidence session (Session 8), not resolved here.
- No credentials, tokens, or `.env` values with real secrets found; `.env.example` only contains placeholder values.

---

## 4. Internal links that will break under the docs restructure

Current link graph (from `README.md` and cross-doc links):

| Link | In | Breaks when |
|---|---|---|
| `docs/ci-cd.md` | `README.md:31,79` | stays — no move planned |
| `k8s/README.md` | `README.md:35,80`, `docs/database-connectivity.md:6` | stays — no move planned |
| `docs/database-connectivity.md` | `README.md:39,82` | **breaks** — renamed to `docs/networking.md` per plan Phase 3 |
| `terraform/README.md` | `README.md:43,81`, `docs/database-connectivity.md:5,147` | stays — no move planned |
| `docs/troubleshooting.md` | `README.md:47,83` | **breaks** — renamed to `docs/operations/runbook.md` |
| `docs/future-improvements.md` | `README.md:51,84` | **breaks** — renamed to `docs/roadmap.md` |
| `docs/proof.md` | `README.md:85` | **breaks** — content folds into README Evidence section + `docs/evidence/`; this link should be removed, not redirected |
| `terraform/modules/eks/README.md` | `docs/database-connectivity.md:68` | stays, but the referring file moves (see above) — link target itself is unaffected, just update the relative path if `networking.md` changes directory depth (it won't; same `docs/` level) |
| `../README.md` | `backend/README.md:3,54`, `frontend/README.md:3,40` | stays — root README path unchanged |

Net: 3 broken links to fix (`database-connectivity.md` → `networking.md`, `troubleshooting.md` → `operations/runbook.md`, `future-improvements.md` → `roadmap.md`), plus the `proof.md` link that should be deleted outright rather than redirected. All are contained to `README.md`'s Documentation table and task-by-task section (already being rewritten in Session 6 regardless).

No links currently point at anything under `docs/decisions/`, `docs/evidence/`, or `docs/operations/` — those are new, nothing to break.

---

## 5. Undocumented design decisions → ADR candidates

Confirmed in code/config, matching (and grounding) the plan's Phase 4 table:

| # | Decision | Where it's visible |
|---|---|---|
| 0001 | Kustomize over Helm | No Helm anywhere in the repo (`grep -ri helm` returns nothing outside the plan doc itself) — pure Kustomize base+overlays in `k8s/` |
| 0002 | OIDC federation over long-lived cloud credentials | `.github/workflows/deploy.yml:172,207,301` (comments), `terraform/modules/eks/iam.tf:63-80` (OIDC provider + IRSA setup), `terraform/modules/eks/outputs.tf:22-34` |
| 0003 | Security-group-to-security-group over CIDR-block rules | Referenced in `README.md:39`, detailed in `docs/database-connectivity.md` — needs the actual SG rule resources cited (`terraform/modules/eks/security.tf`, `terraform/modules/rds/*`) |
| 0004 | Secrets Manager over Terraform-managed secrets | `terraform/modules/rds/main.tf:54` + `outputs.tf:22-24` — RDS-managed master password, `master_user_secret_arn` output, Terraform never sees the plaintext; `prevent_destroy` also lives here and on EKS (`terraform/modules/eks/main.tf:53`, `terraform/modules/rds/main.tf:84`) — worth folding into the same or a sibling ADR |
| 0005 | Default-deny NetworkPolicy posture | `k8s/base/network-policies.yaml` |
| 0006 | Multi-arch images + Trivy gate | `.github/workflows/deploy.yml` build-and-push + Trivy steps (lines ~101-134) |
| 0007 | Ephemeral kind cluster over persistent staging | `.github/workflows/deploy.yml:202-224` ("Real deploy onto an ephemeral kind cluster created inside the runner") |
| 0008 | Custom Terraform modules over registry modules | All of `terraform/modules/{network,eks,ecr,rds,monitoring}` are hand-written, no `source = "terraform-aws-modules/..."` anywhere |

Additional candidate not in the original list, found during this pass:
- **0009 (proposed): S3-native locking over DynamoDB for state locking** — `terraform/backend.tf` header comment explains the choice (`use_lockfile`, Terraform ≥ 1.10) over a DynamoDB lock table, with the legacy alternative documented in `terraform/README.md` section 2. Worth its own ADR since it's a specific, defensible tradeoff most reviewers will not have seen before.
- **0010 (proposed): Mocked ECR/production push over a real cloud account** — `.github/workflows/deploy.yml` explicitly labels the ECR step `[MOCK]` and documents why (no real AWS account backing this repo); `docs/ci-cd.md:78-90` already has the prose, it just isn't framed as a decision record anywhere. This is also the single most likely thing a reviewer probes in an interview, so it earns a direct ADR rather than being buried in `ci-cd.md`.

---

## GitHub state (read-only, via `gh`)

- Repo: `iAhmedMusa/devops-assessment`, default branch `main`, description currently empty, no topics set.
- Releases: six tags exist, `v0.1.0` → `v0.3.0` (`v0.1.0, v0.1.1, v0.1.2, v0.2.0, v0.2.1, v0.3.0`), latest is `v0.3.0`.
- Workflow: one active workflow, `CI/CD`.
- Last 5 runs: all `completed` / `success`, most recent tied to the proof-screenshot and README-rewrite PRs.
