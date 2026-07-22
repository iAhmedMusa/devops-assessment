# Repo Revamp Plan — `devops-assessment` → **Plinth**

**Goal:** reframe a completed assessment as a self-directed reference implementation that demonstrates cloud/DevOps engineering judgement. Content stays; narrative, structure, and evidence change.

**Audience:** hiring managers and senior engineers who spend 90 seconds on the README and then either open `terraform/` or close the tab.

---

## Phase 0 — Decisions (LOCKED — do not re-litigate)

| Decision | Value |
|---|---|
| **Repo name** | `plinth` |
| **Project name** | Plinth |
| **Tagline** | *The base layer your workloads stand on.* |
| **Repo description** | Plinth — a production-shaped AWS platform foundation. Terraform-provisioned VPC/EKS/RDS, Kustomize overlays across four environments, OIDC-federated release pipeline with vulnerability gating and manual production approval. |
| **Topics** | `kubernetes` `terraform` `aws` `eks` `platform-engineering` `infrastructure-as-code` `devops` `cicd` `github-actions` `docker` |
| **Framing rule** | Never write "task", "assessment", "requirement", "was asked to". Write "the problem", "the constraint", "the tradeoff". |
| **Branch** | All work on `revamp/plinth`, merged via a single PR. The PR itself is a work sample — write a real description. |

### Naming rationale (use this in the README and in interviews)

A plinth is the stone base a structure stands on — invisible when the building works, and the reason it stands at all. That is what this repository is: the platform layer beneath a workload, not the workload itself. The Next.js + FastAPI app exists only to have something real to carry.

Names deliberately rejected for collision in this ecosystem: `cloudflow` (Lightbend's Kubernetes streaming project), `bedrock` (AWS), `atlas` (HashiCorp), `keel`, `quay`, `harbor`.

### Naming conventions once renamed

- Product name capitalised in prose: **Plinth**
- Repo, module prefixes, and image names lowercase: `plinth`, `plinth-backend`, `plinth-frontend`
- Kubernetes namespaces: `plinth-local`, `plinth-staging`, `plinth-production`
- Terraform state keys: `plinth/<env>/terraform.tfstate`
- Do **not** rename Docker Hub repos or ECR paths without updating every workflow reference and the k8s overlays — grep for the old name before assuming a rename is complete.

---

## Phase 1 — Root README rewrite (highest leverage, do first)

Delete the task-by-task section entirely. Replace with this structure:

```
1. Title + one-line positioning + badge row
2. Architecture diagram (Mermaid, renders inline on GitHub)
3. "What this demonstrates" — 6-8 bullet capability matrix
4. Quick start (keep as-is, it's good)
5. Design decisions — table linking to ADRs
6. Repository map — annotated tree
7. Evidence — screenshots, CI runs, scan output
8. Docs index
9. About the author
```

### 1.1 Header and positioning

```markdown
# Plinth

*The base layer your workloads stand on.*

[badge row]
```

Then the positioning paragraph. Replace `User profile manager — Next.js frontend, FastAPI backend...` with something that leads with the infrastructure, because the app is not the point:

> Plinth is a production-shaped platform foundation on AWS: Terraform-provisioned VPC, EKS and RDS; Kustomize-managed workloads across four environments; and a release pipeline with OIDC federation, multi-arch builds, vulnerability gating, and a manual production approval gate. A small Next.js + FastAPI application rides on top as the workload under management — it exists to give the platform something real to carry.

Include the one-line naming rationale near the top. It costs a sentence and gives a reviewer something to remember the repo by:

> *A plinth is the base a structure stands on — invisible when the building works, and the reason it stands at all.*

### 1.2 Badge row

CI status (already have), plus: license, Terraform version, Kubernetes version, "Trivy scanned", last release. Use shields.io.

### 1.3 Capability matrix

Table with three columns: **Capability | Implementation | Where**. Rows: container build, orchestration, IaC, secrets management, network isolation, supply-chain security, observability, release strategy. Each "Where" cell links to the actual file, not a doc.

### 1.4 Repository map

Annotated tree in a code block, one line of purpose per directory. Reviewers navigate from this.

---

## Phase 2 — Diagrams

All Mermaid, committed as fenced blocks so they render natively on GitHub and stay diffable. Minimum four:

1. **System architecture** (`README.md`) — VPC three-tier layout, EKS node group, RDS in private subnet, ingress path, security group boundaries. Use Mermaid `flowchart` with `subgraph` per tier.
2. **CI/CD pipeline** (`docs/ci-cd.md`) — PR path vs tag path, with the approval gate and the branch point clearly marked. `flowchart LR`.
3. **Network / traffic flow** (`docs/database-connectivity.md`) — request from browser to Postgres, annotated with what blocks unauthorized traffic at each hop (NetworkPolicy, SG-to-SG, ClusterIP-only). This is the diagram that proves depth.
4. **Environment promotion** (`k8s/README.md`) — base + four overlays, what differs at each.

Optional fifth: Terraform module dependency graph (`terraform/README.md`), generated from `terraform graph` then hand-simplified.

**Rule for Claude Code:** validate every Mermaid block renders before committing — GitHub silently shows a parse error box otherwise. Keep node labels short; long labels break layout on mobile.

---

## Phase 3 — Docs restructure

Current `docs/` is flat and named after tasks. Reorganize by concern:

```
docs/
├── architecture.md          # system overview, tiers, data flow, tradeoffs
├── ci-cd.md                 # keep, add pipeline diagram + threat model of the pipeline
├── database-connectivity.md # rename → networking.md, broaden scope
├── operations/
│   ├── runbook.md           # from troubleshooting.md — reframe as an on-call runbook
│   ├── disaster-recovery.md # RTO/RPO targets, restore procedure
│   └── upgrades.md          # EKS + node group + Terraform upgrade paths (pull from terraform README)
├── decisions/               # ADRs — see Phase 4
└── roadmap.md               # from future-improvements.md
```

Reframing notes:
- `troubleshooting.md` → **runbook**: same 15 scenarios, but structured as *Symptom → Triage commands → Likely causes → Fix → Prevention*. That format is what real SRE runbooks look like and reads as experience rather than a quiz answer.
- `future-improvements.md` → **roadmap**: keep the seven items, add a Now/Next/Later grouping and an honest "why this isn't built yet" line each. Honesty about scope reads as senior.
- `proof.md` → folds into README Evidence section + `docs/evidence/`.

---

## Phase 4 — ADRs (the single biggest credibility signal)

Add `docs/decisions/` with 6–8 short ADRs. Format: Context / Decision / Alternatives considered / Consequences. Keep each under 400 words.

Candidates drawn from what's already built:

| ADR | Decision to document |
|---|---|
| 0001 | Kustomize over Helm for environment overlays |
| 0002 | OIDC federation over long-lived cloud credentials in CI |
| 0003 | Security-group-to-security-group rules over CIDR blocks |
| 0004 | Secrets Manager over Terraform-managed secrets (`prevent_destroy` rationale) |
| 0005 | Default-deny NetworkPolicy posture |
| 0006 | Multi-arch images + Trivy gate in the release path |
| 0007 | Ephemeral kind cluster for staging verification over a persistent staging env |
| 0008 | Custom Terraform modules over community registry modules |

Anyone can apply a manifest. Explaining *why not the alternative* is what separates the levels.

---

## Phase 5 — Evidence

Reviewers rarely run the code. Give them proof they can see in the browser.

- `docs/evidence/` with PNGs: the running UI, a green pipeline run, `kubectl get pods -o wide` across namespaces, Trivy scan summary, `terraform plan` output, the manual approval gate in GitHub UI.
- Embed 3–4 of these in the README, rest linked.
- Link to an actual successful Actions run and a GitHub Release.
- Optional but strong: an asciinema cast of `docker compose up` → working app in under 60s, linked from Quick start.

**Redact before committing:** AWS account IDs, ARNs, real hostnames, IPs, any registry paths tied to a private account.

---

## Phase 6 — Repo hygiene

- `LICENSE` — MIT
- `CONTRIBUTING.md` — short; signals the repo is treated as a product
- `SECURITY.md` — disclosure policy
- `.github/ISSUE_TEMPLATE/` + `PULL_REQUEST_TEMPLATE.md`
- `.github/dependabot.yml` — Actions, pip, npm, Docker
- `CHANGELOG.md` — backfill from the six existing releases
- Pin all GitHub Actions to commit SHAs, not tags (supply-chain hygiene reviewers notice)
- Add `pre-commit` config: `terraform fmt`, `tflint`, `hadolint`, `yamllint`
- Consider adding `checkov` or `tfsec` to CI — one more security gate, cheap to add

---

## Phase 7 — Rename and GitHub metadata (`gh` CLI)

Claude Code has authenticated `gh` access and can execute this phase directly. Two rules:

1. **Confirm with the user before the rename itself.** It changes a public URL and invalidates any local clone remote. Everything after the rename is safe to run unattended.
2. **Rename last, after the code-level rename is done and merged.** Renaming the repo while the code still says `devops-assessment` leaves an inconsistent state.

### 7.1 Verify the name is free

```bash
gh repo view iAhmedMusa/plinth 2>&1 | head -1   # expect a "Could not resolve" error
gh search repos plinth --limit 10               # sanity-check nothing prominent in infra owns it
```

If `iAhmedMusa/plinth` already exists, stop and report back rather than picking a fallback.

### 7.2 Code-level rename (before the repo rename)

```bash
# Audit first — never blind sed
grep -rIn --exclude-dir=.git -e 'devops-assessment' -e 'devops_assessment' -e 'DevOps Assessment' .
```

Review every hit by hand. Expect them in: `README.md`, `docker-compose.yml`, `.github/workflows/*.yml` (image names, kind cluster name), `k8s/**` (namespaces, labels, image refs), `terraform/**` (tags, state keys, resource names, tfvars), `backend/` and `frontend/` config.

**Terraform state keys and live AWS resource names are the dangerous ones** — changing a `name` on a provisioned resource forces replacement. If any infrastructure is currently live, leave live resource names alone and only change tags and documentation; note the discrepancy in an ADR rather than causing a destroy/recreate.

Verify after: `docker compose up -d --build` still works, `kubectl kustomize k8s/overlays/local` still renders, `terraform validate` passes in each env.

### 7.3 Rename the repo and set metadata

```bash
# CONFIRM WITH USER FIRST
gh repo rename plinth --repo iAhmedMusa/devops-assessment

gh repo edit iAhmedMusa/plinth \
  --description "Plinth — a production-shaped AWS platform foundation. Terraform-provisioned VPC/EKS/RDS, Kustomize overlays across four environments, OIDC-federated release pipeline with vulnerability gating and manual production approval." \
  --add-topic kubernetes \
  --add-topic terraform \
  --add-topic aws \
  --add-topic eks \
  --add-topic platform-engineering \
  --add-topic infrastructure-as-code \
  --add-topic devops \
  --add-topic cicd \
  --add-topic github-actions \
  --add-topic docker \
  --enable-issues \
  --enable-wiki=false
```

Then update the local remote:

```bash
git remote set-url origin git@github.com:iAhmedMusa/plinth.git
git remote -v
```

### 7.4 Post-rename verification

```bash
gh repo view iAhmedMusa/plinth
gh workflow list --repo iAhmedMusa/plinth
gh run list --repo iAhmedMusa/plinth --limit 5      # confirm CI still green after rename
gh release list --repo iAhmedMusa/plinth            # six releases should survive the rename
```

Badge URLs in the README contain the repo name — grep and fix them, then confirm each badge actually renders rather than showing "invalid".

### 7.5 Remaining polish

```bash
gh release create v1.0.0 --repo iAhmedMusa/plinth \
  --title "Plinth v1.0.0" \
  --notes-file CHANGELOG-v1.0.0.md
```

- Pin the repo on the GitHub profile (`gh` cannot do this — manual, Profile → Customize your pins)
- Social preview image (manual, Settings → Social preview) — export the architecture diagram
- Optional: add a `GET /metrics` Prometheus endpoint to the backend, so the roadmap's observability item is partly real rather than entirely aspirational

---

## Execution order for Claude Code

Run as separate sessions, commit after each — do not attempt in one pass.

```
Session 1  Audit — read everything, produce docs/_audit.md. No file changes.
Session 2  Phase 7.2 — code-level rename to Plinth. Verify builds still work.
Session 3  Phase 3 — docs restructure + renames (git mv, preserve history).
Session 4  Phase 2 — write and validate all Mermaid diagrams.
Session 5  Phase 4 — ADRs, drafted from what the code actually does.
Session 6  Phase 1 — README rewrite, once everything it links to exists.
Session 7  Phase 6 — hygiene files + CI additions.
Session 8  Phase 5 — evidence capture (manual: you take the screenshots).
Session 9  Merge PR, then Phase 7.1/7.3/7.4/7.5 — repo rename via gh, tag v1.0.0.
```

### Opening prompt for Session 1

> Read this entire repository. Produce `docs/_audit.md` containing: (1) every file and line that frames this as an assessment, test, or task-completion exercise, with a suggested replacement phrasing; (2) every occurrence of `devops-assessment` / `DevOps Assessment` in any form, grouped by risk — safe to rename, needs care (image refs, k8s namespaces, CI workflow references), and do-not-touch (anything tied to live AWS resource names or Terraform state keys); (3) any file containing account IDs, ARNs, IPs, hostnames, or credentials needing redaction before this is a public portfolio piece; (4) all internal links, flagging any that break under the restructure in REPO-REVAMP-PLAN.md; (5) design decisions visible in the code that are not explained anywhere — these become ADRs. Do not modify any files. You have `gh` access; use it read-only this session to list releases, workflow runs, and current repo settings.

### Standing instructions for every session

- Work on branch `revamp/plinth`. Commit at the end of each session with a descriptive message.
- Never run destructive `gh` commands (`repo delete`, `release delete`, force-push to `main`).
- Confirm with the user before: the repo rename, deleting any file, and any change to live infrastructure resource names.
- After every session, re-run `docker compose up -d --build` and `kubectl kustomize k8s/overlays/local` to confirm nothing was broken by documentation work.

Keep `REPO-REVAMP-PLAN.md` at the repo root during the work; delete it in the final commit before merge.

---

## What to resist

- Don't inflate. "Production-shaped" and "reference implementation" are honest; "production system serving X users" is not, and a senior reviewer will probe it in the interview.
- Don't delete the assessment history from the git log. 52 commits with real progression is itself evidence. Only the *presentation* changes.
- Don't add tech just to widen the stack. A tight, well-justified stack beats a wide, thin one.
