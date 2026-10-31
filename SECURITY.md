# Security Policy

## Supported versions

Only the latest release series is maintained. Version 0.1.0 is an
**experimental local reference**, not a production security boundary.

## Reporting a vulnerability

Do **not** disclose exploit details, personal data or secrets in a public issue.
Before releasing the repository, the maintainer must configure a private
security-advisory reporting channel for the repository (for example, the
repository's private vulnerability reporting feature) and document it here.
Until then, this package is **not ready for public security intake**.

We welcome reproducible, local-only minimal reproductions using synthetic
files. Do not test other people's infrastructure without authorization.

## Explicit non-guarantees

No hardening against an adversary with write privileges to the host process,
workspace parent, package source or evidence database. See
[docs/THREAT_MODEL.md](docs/THREAT_MODEL.md).
