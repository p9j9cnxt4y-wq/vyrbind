# ForgeProofGate 0.1.0 — unreleased candidate verification

Date: 2026-10-31. Ticket: VYFORGE-FORGEPROOFGATE-CI-PORTABILITY-003.
Scope: existing local repair plus corrected release documentation. No public release.
Version 0.1.0 is a package version, not a unique source identity or a release claim.

## Current local verification scope

Windows results below cover targeted code, unit, regression, negative and smoke
checks of this candidate. They are **not complete functional product acceptance**.
The product code and test bytes retain the locally verified Junction/ledger fix;
documentation changes require a new full source map and new built artifacts.

| Environment | Discovered | Passed | Skipped | Test exit | Smoke exit |
| --- | ---: | ---: | ---: | ---: | ---: |
| Windows / Python 3.12.10 source | 47 | 46 | 1 | 0 | 0 |
| Windows / Python 3.13.13 source | 47 | 46 | 1 | 0 | 0 |
| Windows / Python 3.15.0 source | 47 | 46 | 1 | 0 | 0 |
| Windows / Python 3.13.13 installed wheel | 47 | 46 | 1 | 0 | CLI below |

Commands: `python tools/verify.py` and `python tools/smoke.py`. The installed-wheel
suite imports the installed package, not the source checkout. Its CLI create and
artifact readback exit 0; a deployment request returns `HUMAN_GATE_REQUIRED` with
expected exit 2 and no deployment effect; chain-only verification exits 0.

One test per local suite is skipped because the fixture volume does not provide
distinct case-sensitive sibling directory names. The case-alias, real symlink
and Windows junction tests do run. Platform-dependent skips must be recorded
again in CI; a skip is not a passed test. Python 3.11 is declared as the minimum
but has not been run locally for this correction. Local Python 3.15 does not
replace a Python 3.11 CI result.

The 13 added boundary tests include inside-ledger rejection through real
ancestor aliases and `..`, nested containment, allowed external audit readback,
case behavior and preservation of untracked-node/artifact and direct link guards.
Four of them failed against the unchanged starting validator. Real baseline
traces showed premature SQLite creation followed by `UNTRACKED_NODE_IN_WORKSPACE`;
the repair rejects inside audit-file paths before lock/ledger creation with
`AUDIT_INSIDE_WORKSPACE`. No alternative error code is accepted by these tests.

## Offline package verification

- Two local wheel builds with fixed SOURCE_DATE_EPOCH and no package index,
  dependency download or build isolation produce identical wheel bytes in the
  tested environment. This is not a reproducibility guarantee across environments.
- Wheel CRC and all 12 RECORD entries are verified; six package modules match
  source bytes. Metadata declares version 0.1.0, MIT and no runtime dependencies.
- The source ZIP contains all 27 candidate files. The 26-entry source manifest
  covers every candidate file except itself. The accompanying source map covers
  all 27 files, including the manifest. Candidate assets have separate SHA-256s.
- Source and installed-wheel negative tests, source smokes and installed CLI
  readback are rerun after the documentation update. New hashes supersede earlier
  candidate identities; original kits and previous evidence remain historical.

Exact commands, actual exit codes, logs, source-map/diff hashes and artifact hashes
are retained in the accompanying local review bundle. Only its final verified
candidate identity may be proposed for the new commit/push gate. A previous
wheel or source archive with the same version must not be substituted.

## Historical evidence — does not verify the current candidate

1. Original kit: Windows / Python 3.12.10 discovered 32 tests with two SQLite
   connection-cleanup errors; smoke exit 0. Original ZIP CRC, archive paths,
   manifests, wheel RECORD and source-module correspondence were checked before
   staging. A targeted scan of the original 25 source files found no credential/
   private-path matches; that result does not cover newly changed bytes.
2. Earlier local pre-publication baseline: Windows / Python 3.13.13 passed 34
   tests with zero skips; smoke exit 0. Its added tests cover nested JSON
   rejection and a real workspace junction. These results belong to commit
   `3af0952b319fca452a27d2967f1cbce47c7ac399`, before the audit-containment repair.
3. Historical GitHub Actions run **41193942446**, attempt 1, on that same commit:
   Linux 3/3 jobs succeeded; Windows 0/3 and macOS 0/3 succeeded. The six failed
   jobs expected `AUDIT_INSIDE_WORKSPACE` but got `UNTRACKED_NODE_IN_WORKSPACE`.
   The overall run failed. Logs do not establish the exact alias spelling of
   those hosted runners. Local reproduction proves the validator defect, not
   a particular historical runner configuration.
4. The first repair-only local candidate passed targeted Windows checks, but
   carried stale release documentation. Its evidence and hashes remain valid
   only for that historical candidate, not this documentation-complete one.
5. Historical Linux build/install results in the original kit apply only to
   that original kit; they cannot verify new corrections.

## Current platform and release limits

- **Linux:** new corrections are functionally unconfirmed; new-candidate CI NOT_RUN.
  Historical success applies only to the exact earlier commit above.
- **macOS:** new corrections are functionally unconfirmed; new-candidate CI NOT_RUN.
- **Windows:** targeted checks in the listed local environments only, not full
  functional acceptance or a successful new Windows GitHub Actions run.
- **GitHub Actions PASS** means only that the documented tests of that specific
  commit passed in the recorded environment. A configured 3x3 matrix is a plan,
  not execution evidence. No general defect freedom, complete sandbox security,
  production readiness or guaranteed cross-platform compatibility is claimed.
- Host-controlled parents and audit storage remain prerequisites. Path checks
  are not race-free against a hostile filesystem actor. Audit hashes are not
  signatures; content is not reliably screened for secrets. See the threat model.
- FORGEPRIME host integration remains NOT_VERIFIED and is not supplied or
  required by this standalone contract.
- A private repository and the old baseline push are historically documented.
  Account, remote tip and private visibility require fresh readback before any
  newly authorized write. No new commit, push or CI run is authorized here.
- Public visibility, tags and release remain blocked until separate Gate B.
  Publisher attribution, name clearance and a verified private vulnerability
  reporting channel remain publication prerequisites. MIT metadata is not
  independent legal or provenance clearance.

FORGE_READY != EXECUTION_AUTHORIZED. See [PUBLISHING.md](PUBLISHING.md) for draft
release notes and the distinct owner gates.
