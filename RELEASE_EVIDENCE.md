# VyrBind 0.1.0 — verification scope and source identity

> **Private VyrBind qualification (unreleased):** commit
> `9815abaf2bf872c8ea71ad3c7f9db80daeccbc1f` passed all nine jobs in
> GitHub Actions run `41258404480`. This is fixed historical evidence, not
> a CI claim for later revisions or full platform/security acceptance.
> Final commit, CI and asset bindings belong to the external release record.


Version 0.1.0 alone does not identify source bytes or establish that a release
exists. For a published release, use its tag target, attached SHA256SUMS.txt and
release verification record. Before publication these records are local drafts.
This file records fixed historical evidence; it does not contain its own commit
SHA or claim that a later revision automatically passed CI.

## Completed private VyrBind integration

Commit `9815abaf2bf872c8ea71ad3c7f9db80daeccbc1f` was privately pushed and
independently read back after the namespace/CLI rename. Run `41258404480`,
attempt 1, passed all nine Windows/Linux/macOS jobs with Python 3.11/3.12/3.13.
All 27 remote files matched the approved VyrBind candidate. Each Windows job
discovered 47 tests, passed 46 and skipped one; each Linux/macOS job discovered
47, passed 45 and skipped two. Source regression and clean-room smoke passed
in every job. Skip reasons are the filesystem and Windows-junction limitations
listed below; skipped checks are not passes.

Fresh local Windows source tests for that integration passed 46 of 47 checks
with one filesystem skip; smoke exited 0. All nine full logs for that run were
read and subjected to targeted privacy checks with no unresolved finding.
Raw logs and private review evidence are not publication assets. This is a
scoped review and not proof of universal absence of sensitive content.

Security-contact and subsequent documentation corrections do not inherit this
whole-commit CI result. Their exact final commit, CI run and ZIP/wheel hashes
must be recorded externally after their own approved private integration.

## Historical pre-rename private qualification baseline

Commit `d9490644694d108d85a844ed1d9efeb72c64176c` was privately pushed and
independently read back. GitHub Actions run `41253469293`, attempt 1, completed
all nine jobs successfully. All 27 remote source files matched the approved
candidate. This is the completed START-002 baseline, not a public release.

| CI environment | Python per job | Discovered | Passed | Skipped |
| --- | --- | ---: | ---: | ---: |
| Windows | 3.11 / 3.12 / 3.13 | 47 | 46 | 1 |
| Linux | 3.11 / 3.12 / 3.13 | 47 | 45 | 2 |
| macOS | 3.11 / 3.12 / 3.13 | 47 | 45 | 2 |

Windows skips distinct case-sensitive sibling names on its fixture volume.
macOS skips those siblings and the Windows-only junction fixture. Linux skips
the unavailable case-alias fixture and the Windows-only junction fixture.
A skip is not a pass. Source regression and clean-room smoke steps succeeded
in every job. Successful logs do not separately emit numeric process exit codes.

The source and installed-wheel checks bound to the same approved baseline
on local Windows/Python 3.13.13 recorded 47 discovered, 46 passed and one skip.
Source verification, smoke, offline wheel build/install, CLI creation and chain
verification exited 0; the intentional deployment refusal exited 2.
The closeout reuses unchanged runtime/test evidence only after checking hashes.
A rebuilt wheel with changed README metadata requires fresh package integrity
and isolated installation checks; it does not require relabeling old tests.

## Earlier history

- Commit `1e781555e7ff6ab6a93c97146aa3136c3ade4ff0`, run `41203391771`:
  nine successful jobs with the same 47/46/1 Windows and 47/45/2 Linux/macOS
  counts. It supplied the audit-parent containment correction.
- Commit `3af0952b319fca452a27d2967f1cbce47c7ac399`, run `41193942446`:
  three Linux jobs succeeded; six Windows/macOS jobs failed because the tests
  expected AUDIT_INSIDE_WORKSPACE but received UNTRACKED_NODE_IN_WORKSPACE.
  This historical failure is retained and is not relabeled as success.
- Original-kit 32-test and earlier 34-test results describe earlier sources,
  not the 47-test qualification baseline.

CLOSEOUT-003 read all 27 complete job logs across these three runs and reviewed
the reachable three-commit history. Targeted credential, identity and private
infrastructure checks found no unresolved publication-sensitive match.
GitHub-hosted runner paths and masked checkout credentials were classified
separately. This is a scoped review, not proof that arbitrary secrets cannot
exist. Raw logs and private review records are not release assets.

## Final release binding

Documentation corrections after the qualification baseline do not inherit a
whole-commit CI PASS. Before publishing, a separately approved final private
commit must match the reviewed source map and pass its configured nine jobs.
Record that exact commit, run, skips and asset hashes outside the committed
source, in the release verification record. Do not commit a new SHA merely to
update this file. Any changed source bytes invalidate the previous candidate
binding; re-evaluate only the affected checks.

## Technical limits

CI success establishes only the tests executed for that commit and environment.
It does not establish full platform acceptance, general compatibility, defect
freedom, production readiness or complete sandbox security. Python >=3.11 is a
declared minimum, not evidence for every interpreter/platform combination.

The broker requires trusted host-controlled directories and runtime. It is not
race-free against hostile filesystem writers; audit hashes are not signatures
and artifact content is not reliably screened for secrets. FORGEPRIME-FPP host
integration is NOT_VERIFIED and is neither supplied nor required by this
standalone contract. See [the threat model](docs/THREAT_MODEL.md).

Publication and confidential reporting remain separately gated as described in
[PUBLISHING.md](PUBLISHING.md) and [SECURITY.md](SECURITY.md).
FORGE_READY != EXECUTION_AUTHORIZED.
