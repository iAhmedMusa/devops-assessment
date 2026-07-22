# Security policy

## Scope

This repo has no live deployment and no production data — Terraform
here has never been applied against a real AWS account (see
`terraform/README.md` section 9). A vulnerability here is one that would
matter if this configuration *were* applied for real: a NetworkPolicy
gap, an over-broad IAM policy, a security group that admits more than
it should, a secret handling mistake, or a supply-chain issue in the
CI pipeline.

## Reporting a vulnerability

Please use [GitHub's private vulnerability reporting](../../security/advisories/new)
for this repository rather than opening a public issue. If that's not
available, open an issue without exploit details and note that you
have a security report, so it can be moved to a private channel.

Include:
- What you found and where (file/line if applicable).
- What a real deployment would let an attacker do with it.
- A suggested fix, if you have one — not required.

## Response

This is a solo-maintained portfolio project, not a monitored production
service — there's no SLA, but reports are read and acknowledged. Fixes
for anything affecting the patterns this repo demonstrates (not just a
typo) are prioritized over feature work.

## What's already covered

Known, disclosed tradeoffs — a mocked production deploy, a single-AZ
database by default, report-only vulnerability scanning — are
documented in [`docs/decisions/`](docs/decisions/) and
[`docs/roadmap.md`](docs/roadmap.md). Those aren't vulnerabilities to
report; they're deliberate scope decisions explained in place.
