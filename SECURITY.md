# Security Policy

## Scope and supported versions

VyrBind 0.1.0 is an experimental local reference, not a production
security boundary. No maintenance SLA or complete platform acceptance is
asserted. Release availability and exact tested bytes are identified by the
release record; see [RELEASE_EVIDENCE.md](RELEASE_EVIDENCE.md).

## Reporting a vulnerability

Do **not** put exploit details, personal data or secrets in public issues.

The preferred confidential route is **GitHub Private Vulnerability Reporting**.
On this repository's Security / Advisories page, use **Report a vulnerability**
only when GitHub presents the private reporting form. This policy does not
assert that reporting is already enabled. Activation and reporter-facing
verification must precede a public release.

If the private form is unavailable, do not post sensitive details publicly.
No alternative security address is currently confirmed in this policy. An
existing owner-confirmed security address may be added after its responsible
recipient and reachability are verified; no address is inferred from the brand.

Provide affected version/commit, impact and a minimal local reproduction using
synthetic data. Do not send credentials or test other people's infrastructure.
The maintainer must verify the selected route and notification handling before
release. No test report or contact message is implied by this policy.

## Explicit non-guarantees

This package does not harden against an adversary with write access to the host
process, workspace parent, package source or evidence database. It does not
provide OS isolation, authenticated audit signatures, reliable secret screening
or general race freedom. See [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md).
