# Changelog

## 0.1.0 — unreleased candidate, 2026-10-31

- Check physical audit-parent ancestry before creating any lock or ledger;
  ancestor aliases and `..` cannot hide an audit file inside the workspace.
- Preserve original I/O paths, direct symlink/reparse guards and both untracked
  node/artifact guards. No alternate error code is accepted for inside-ledger tests.
- Add 13 real-filesystem boundary tests and strengthen the original ledger test.
- Correct DE/EN platform, test, CI and release claims; distinguish a declared
  Python minimum from verified combinations and historical CI from the new candidate.
- Windows targeted checks: 47 discovered, 46 passed, one filesystem-dependent
  skip per tested interpreter; no complete functional product acceptance.
- New Linux/macOS corrections remain functionally unconfirmed. GitHub Actions
  PASS applies only to documented tests of the exact tested commit/environment.
- No public release, production-readiness or general compatibility claim.

## Historical 0.1.0 pre-publication baseline — 2026-10-31

These earlier changes belong to commit
`3af0952b319fca452a27d2967f1cbce47c7ac399`, not a published release:

- Close SQLite test connections explicitly for Windows cleanup.
- Redact excessive JSON nesting as a blocked parse result, with regression coverage.
- Reject workspace reparse points using Windows file attributes, with a real junction test.
- Require a build backend supporting SPDX license expressions and include the MIT license explicitly.
- Clarify local SQLite effects and distinguish current verification from historical package evidence.

## Historical initial 0.1.0 source — 2026-10-29 (not a release claim)

- Initial local-only, fail-closed deterministic broker.
- Strict intent schema, run/scope binding, exclusive create, readback.
- Digest-only SQLite audit chain, tamper checks and operator recovery stops.
- Documented boundaries and local negative tests.
- No external tool, network, deploy, training or approval issuance paths.
