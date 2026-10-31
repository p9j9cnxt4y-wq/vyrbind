# ForgeProofGate 0.1.0 — verification scope and source identity

This is an uncommitted local attribution/documentation candidate based on
`1e781555e7ff6ab6a93c97146aa3136c3ade4ff0`. Package version 0.1.0 is not a unique
source identity or a claim that a release exists. Runtime code, tests and CI
workflow are unchanged; new copyright/metadata/documentation bytes require
new source and asset hashes.

## Retained evidence for the base commit

The preserved execution record reports GitHub Actions run `41203391771`,
attempt 1, nine successful jobs on the exact base commit above. This record
was checked locally for integrity; fresh remote readback and complete remote
historical log inspection are NOT_RUN in this local-only preparation.

| Recorded CI environment | Python per job | Discovered | Passed | Skipped |
| --- | --- | ---: | ---: | ---: |
| Windows | 3.11 / 3.12 / 3.13 | 47 | 46 | 1 |
| Linux | 3.11 / 3.12 / 3.13 | 47 | 45 | 2 |
| macOS | 3.11 / 3.12 / 3.13 | 47 | 45 | 2 |

Windows skips distinct case-sensitive sibling names on the fixture volume.
macOS skips those siblings and the Windows-only junction fixture. Linux skips
the unsupported case-alias fixture and the Windows-only junction fixture.
Skipped tests are not passed tests. Source regression and smoke steps were
recorded as successful; the retained successful CI logs do not separately
emit numeric process exit codes.

Retained local Windows checks of the base source on Python 3.12.10, 3.13.13
and 3.15.0 discover 47 tests, pass 46 and skip one distinct-case sibling
fixture, with source-test/smoke exits 0. The retained installed-wheel suite
on Python 3.13.13 records the same 47/46/1 result; CLI create and chain check
exit 0, and deployment refusal has expected exit 2. These are historical
checks of their bound bytes, not new test runs of changed release metadata.

## Historical failure retained for transparency

Earlier run `41193942446` on commit
`3af0952b319fca452a27d2967f1cbce47c7ac399` failed overall. Three Linux jobs
succeeded; six Windows/macOS jobs expected AUDIT_INSIDE_WORKSPACE but got
UNTRACKED_NODE_IN_WORKSPACE. The later base commit contains the physical
audit-parent containment correction and 13 added real-filesystem tests.
The original kit's 32-test and earlier 34-test results do not describe the
current base suite. No historical failure is relabeled as success.

## Current candidate and limits

No new commit, push, CI run, public visibility or release is authorized.
Local candidate verification and exact asset hashes are recorded in the
separate preflight bundle; private receipts and raw logs are not release files.
Only freshly built, source-bound assets may be proposed for publication.

GitHub CI success establishes only the documented tests of its exact commit
and environment. It does not establish full Windows/Linux/macOS functional
acceptance, general compatibility, defect freedom, production readiness or
complete sandbox security. Python >=3.11 is a declared minimum, not evidence
for untested interpreter/platform combinations.

The broker depends on trusted host-controlled directories and runtime. It is
not race-free against hostile filesystem writers; evidence hashes are not
signatures and artifact content is not reliably screened for secrets.
FORGEPRIME-FPP host integration is NOT_VERIFIED and is neither supplied nor
required by this standalone source contract. No simulation substitutes for it.

Security intake and remaining publication prerequisites must be resolved
before a new Gate B can be requested. FORGE_READY != EXECUTION_AUTHORIZED.
