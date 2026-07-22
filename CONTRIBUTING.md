# Contributing

This is primarily a reference implementation, but PRs that fix a bug,
improve a doc, or tighten something up are welcome.

## Workflow

1. Fork or branch from `main`.
2. Make your change. Keep PRs scoped to one concern — a Terraform fix
   and a docs typo fix are two PRs, not one.
3. Run the relevant checks locally before opening a PR:
   ```bash
   # App
   cd backend && pytest -v
   cd frontend && npm run lint && npm run build

   # Kubernetes
   kubectl kustomize k8s/overlays/local

   # Terraform
   cd terraform && terraform fmt -check -recursive && terraform validate
   ```
4. Open a PR against `main`. CI runs the same checks — a PR with red
   checks won't merge.

## Commit style

Conventional Commits (`fix:`, `feat:`, `docs:`, `ci:`, `chore:`) —
see `git log` for examples already in this repo.

## Scope boundaries

- Terraform here has never been applied against a real AWS account (see
  `terraform/README.md` section 9). Changes should keep `plan` and
  `validate` passing without requiring real credentials — don't add a
  data source that needs a live account to resolve.
- Don't rename live-adjacent identifiers (Terraform resource names,
  state keys) without reading `docs/decisions/` first — several of
  those choices are deliberate, not defaults.
- New design decisions with a real alternative should get a short ADR
  in `docs/decisions/`, not just a code comment.
