# Changelog

All notable changes to this project are documented here, backfilled
from the six GitHub releases published so far. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/).

## [v0.3.0](https://github.com/iAhmedMusa/devops-assessment/releases/tag/v0.3.0) — 2026-07-04

### Added
- Terraform module-based EKS provisioning (design-complete,
  credential-free `plan`, zero real `apply`) — [#12](https://github.com/iAhmedMusa/devops-assessment/pull/12)

## [v0.2.1](https://github.com/iAhmedMusa/devops-assessment/releases/tag/v0.2.1) — 2026-07-04

### Fixed
- Retried the ingress smoke test to absorb nginx config reload lag in
  the ephemeral kind cluster — [#11](https://github.com/iAhmedMusa/devops-assessment/pull/11)

## [v0.2.0](https://github.com/iAhmedMusa/devops-assessment/releases/tag/v0.2.0) — 2026-07-04

### Added
- Real deploy to an ephemeral kind cluster in the staging stage of the
  pipeline — [#10](https://github.com/iAhmedMusa/devops-assessment/pull/10)

### Fixed
- Pinned a numeric `runAsUser` for non-root verification —
  [#8](https://github.com/iAhmedMusa/devops-assessment/pull/8)
- Bumped staging/production image tags to the multi-arch v0.1.2 build —
  [#9](https://github.com/iAhmedMusa/devops-assessment/pull/9)

## [v0.1.2](https://github.com/iAhmedMusa/devops-assessment/releases/tag/v0.1.2) — 2026-07-04

### Added
- Kubernetes manifests and Kustomize overlays (base + local/staging/
  production/ci) — [#6](https://github.com/iAhmedMusa/devops-assessment/pull/6)

### Fixed
- Corrected the `build-push-action` key name to `platforms` —
  [#7](https://github.com/iAhmedMusa/devops-assessment/pull/7)

## [v0.1.1](https://github.com/iAhmedMusa/devops-assessment/releases/tag/v0.1.1) — 2026-07-04

### Fixed
- Published multi-arch images (amd64 + arm64) instead of a single
  platform — [#5](https://github.com/iAhmedMusa/devops-assessment/pull/5)

## [v0.1.0](https://github.com/iAhmedMusa/devops-assessment/releases/tag/v0.1.0) — 2026-07-03

### Added
- Initial CI/CD pipeline with staged deploy gates —
  [#2](https://github.com/iAhmedMusa/devops-assessment/pull/2)

### Fixed
- Frontend edit and delete profile actions —
  [#1](https://github.com/iAhmedMusa/devops-assessment/pull/1)
- Pinned the Trivy action to a valid release, then to a commit SHA —
  [#3](https://github.com/iAhmedMusa/devops-assessment/pull/3),
  [#4](https://github.com/iAhmedMusa/devops-assessment/pull/4)
