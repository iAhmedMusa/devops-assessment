## What this changes and why

<!-- The "why" matters more than the "what" here -- link an issue or ADR if one exists. -->

## Checked locally

- [ ] `backend`: `pytest -v` passes
- [ ] `frontend`: `npm run lint && npm run build` passes
- [ ] `k8s`: `kubectl kustomize k8s/overlays/<affected>` renders cleanly
- [ ] `terraform`: `terraform fmt -check -recursive && terraform validate` passes
- [ ] Docs/links updated if a file moved or a path changed

## Scope

- [ ] This PR does one thing (see `CONTRIBUTING.md`)
- [ ] No live Terraform resource names or state keys were changed without a note in `docs/decisions/`
