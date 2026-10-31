# ForgeProofGate 0.1.0 — pre-publication verification

Date: 2026-10-31. Scope: isolated Windows source verification; no public release.

The original kit is retained separately. This candidate contains reviewed corrections;
it must not be paired with the original unpatched wheel or source archive.

## Fresh results

- Original source on Windows / Python 3.12.10: 32 tests, two cleanup errors caused by SQLite test connections left open. Smoke exit 0.
- Corrected source on Windows / Python 3.13.13: 34 tests passed, no skips, errors or failures; smoke exit 0.
- The two added tests cover deeply nested JSON rejection without traceback or filesystem effects, and refusal of a real Windows junction before audit creation.
- The junction test isolates the reparse-attribute guard from the convenience helper. It does not establish a Python 3.11 runtime result.
- Original ZIP CRC, archive paths, manifests, wheel RECORD and source-module correspondence were checked before staging.
- Targeted credential/private-path scanning of the original 25 source files found no matches; final candidate and built artifacts require their own final scan.

## Publication gates and limits

- GitHub Actions: NOT_RUN. The configured matrix has Windows, Linux and macOS with Python 3.11, 3.12 and 3.13.
- GitHub publication and release: NOT_RUN; separate owner approvals are required.
- FORGEPRIME host integration: NOT_VERIFIED; the standalone kit does not require or supply that integration.
- Rights attribution, name clearance and private security reporting remain unresolved publication checks.
- Historical Linux build/install results in the original kit are not evidence for this candidate.
- This project provides no OS sandbox, authenticated human approval, external executor or signed audit anchor.

Build, wheel-install and release-asset verification are recorded in the separate local
publication review bundle and must be bound to the exact reviewed commit before release.
