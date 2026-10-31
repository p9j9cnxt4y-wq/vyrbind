# Security Policy

## Supported versions

Version 0.1.0 is an unreleased, experimental local reference. It is not a
production security boundary. No supported release series or full platform
acceptance is asserted. See [RELEASE_EVIDENCE.md](RELEASE_EVIDENCE.md).

## Reporting a vulnerability

Do **not** disclose exploit details, personal data or secrets in a public issue.
No existing confidential reporting contact has been confirmed for this
candidate. Public release is blocked until a reachable confidential channel
and responsible recipient are verified and documented here. No contact address
is inferred from the publisher brand.

GitHub private vulnerability reporting is available for public repositories.
Its later activation requires separate owner authorization and readback; it
does not replace the missing pre-publication confidential contact. No report
or test message has been sent as part of this preparation.

Use reproducible, local-only minimal examples with synthetic data. Do not test
other people's infrastructure without authorization.

## Explicit non-guarantees

No hardening against an adversary with write privileges to the host process,
workspace parent, package source or evidence database. See
[docs/THREAT_MODEL.md](docs/THREAT_MODEL.md).
