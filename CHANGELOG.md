# Changelog

## 0.1.0 pre-publication verification — 2026-10-31

- Close SQLite test connections explicitly for Windows cleanup.
- Redact excessive JSON nesting as a blocked parse result, with regression coverage.
- Reject workspace reparse points using Windows file attributes, with a real junction test.
- Require a build backend supporting SPDX license expressions and include the MIT license explicitly.
- Clarify local SQLite effects and distinguish current verification from historical package evidence.

## 0.1.0 — 2026-10-29

- Initial local-only, fail-closed deterministic broker.
- Strict intent schema, run/scope binding, exclusive create, readback.
- Digest-only SQLite audit chain, tamper checks and operator recovery stops.
- Documented boundaries and local negative tests.
- No external tool, network, deploy, training or approval issuance paths.
