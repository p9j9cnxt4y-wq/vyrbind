# Proposed publication metadata and draft release notes

**Repository name:** `forgeproofgate` (provisional; no trademark clearance)  
**Title:** ForgeProofGate — Deterministic Safety Boundary for AI Agents  
**Short description:** A dependency-free Python reference for fail-closed agent tool authorization, bounded local artifact writes, and verifiable readback evidence.  
**Topics:** `ai-agents`, `agent-security`, `policy-engine`, `least-privilege`, `fail-closed`, `python`, `safety-invariants`

## Draft release notes — unreleased v0.1.0 candidate

ForgeProofGate v0.1.0 demonstrates how a limited set of AI-agent safety invariants
can be enforced in ordinary Python code rather than relying on a system
prompt. It rejects unknown tools and out-of-scope actions, allows only new
text artifacts within a pre-bound local workspace, verifies actual effects,
and writes hash-linked audit records. All other effects, including deployment,
network, credentials, and training, remain disabled.

The candidate preserves the physical audit/workspace containment fix: trusted
ancestor aliases and `..` cannot conceal an audit file inside the workspace
before lock/ledger creation. Direct link/reparse and untracked-node/artifact
guards remain. Thirteen additional real-filesystem tests cover this boundary.

Windows verification covers targeted code, unit, regression, negative and smoke
behavior in the recorded scope; it is **not complete functional product acceptance**.
Python 3.12.10, 3.13.13 and 3.15.0 each discover 47 tests: 46 pass, one is skipped
because the fixture volume does not provide distinct case-sensitive sibling
names. Source test/smoke exits are 0. Installed-wheel tests and CLI readback are
also verified; exact package checks and exits are in [RELEASE_EVIDENCE.md](RELEASE_EVIDENCE.md).

Historical Linux CI success belongs only to commit
`3af0952b319fca452a27d2967f1cbce47c7ac399`. New Linux/macOS corrections are
functionally unconfirmed; new-candidate CI is NOT_RUN. A GitHub Actions PASS
means only the documented tests of that specific commit/environment passed.

This is a **local reference implementation**, not an audited firewall,
zero-knowledge system, human-approval service or production-ready AI agent.
No general freedom from defects, complete sandbox security or guaranteed
cross-platform compatibility is claimed. Host trust, protected directories,
race limitations, unsigned audit hashes and unscreened content remain explicit
risks in [the threat model](docs/THREAT_MODEL.md). Version 0.1.0 alone does not
identify the reviewed source or authorize use of older same-version artifacts.

## New owner commit/push gate — not an authorization

Prepare the complete diff, exact file list, fresh source-map and asset hashes,
starting HEAD and planned commit message for review. Earlier gates and older
candidate hashes do not authorize this candidate. After explicit new approval:

1. Recheck the local bytes, index and starting HEAD; authenticate and independently
   read back the exact target repository, private visibility and remote base.
   Stop on any drift or identity mismatch.
2. Create exactly one reviewed local commit. Verify every committed blob against
   the approved candidate before one private fast-forward push; never force-push.
3. Read back the new remote commit/tree and evaluate all nine configured jobs:
   Windows/Linux/macOS with Python 3.11/3.12/3.13, source tests and smoke.
   Record actual test counts, skips, logs and conclusions for that exact commit.
4. Stop on CI failure. An uncertain push requires readback, not blind retries.
   No additional commit, workflow rerun, secrets or repository-setting changes
   are implied by this gate. Public visibility, tags and release remain blocked.

## Separate Gate B — public visibility and release

1. Confirm legal publisher attribution, repository name and MIT license.
2. Enable private vulnerability reporting and replace the note in SECURITY.md.
3. Check the CI matrix passed against the exact proposed release commit; treat
   PASS only as evidence for its documented tests, not product acceptance.
4. Confirm release archive and wheel digests independently.
5. Obtain explicit Gate B for public visibility, tag/release and the exact assets.
   Do not auto-publish, auto-deploy or
   connect production systems as part of this reference release.

FORGE_READY != EXECUTION_AUTHORIZED.
