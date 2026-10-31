# Publication metadata and unreleased release notes

**Repository name:** `forgeproofgate` (provisional; no trademark clearance)
**Project/publisher brand:** vYronFORGE.
**Title:** ForgeProofGate — Limited Python Reference Broker for Agent Actions
**Short description:** A dependency-free Python reference for fail-closed agent tool authorization, bounded local artifact writes, and readback evidence.
**Topics:** `ai-agents`, `agent-security`, `policy-engine`, `least-privilege`, `fail-closed`, `python`, `safety-invariants`

## Draft release notes — unreleased v0.1.0 candidate

ForgeProofGate v0.1.0 is a limited Python reference broker for one local
operation: exclusive creation of a new UTF-8 text file in a host-bound workspace,
followed by artifact readback and hash-linked SQLite evidence. Unknown tools are
denied. Network, deployment, credentials and other controlled effects have no
executor. It is not an OpenAI product, an OS sandbox, a complete AI security
solution, an authenticated human-approval service or a production-ready agent.

Project and publisher brand: **vYronFORGE.**

Copyright (c) 2026 vYronFORGE.

The MIT license terms remain unchanged. The public attribution uses the brand;
it does not declare a legal form or make independent third-party rights claims.

This candidate updates attribution, package metadata and publication documents.
Runtime code, tests and workflow remain byte-identical to commit
`1e781555e7ff6ab6a93c97146aa3136c3ade4ff0`, including its physical audit/workspace
containment correction. Retained evidence for CI run `41203391771` reports nine
successful Windows/Linux/macOS jobs with Python 3.11/3.12/3.13. Each Windows job
records 47 discovered, 46 passed and one skip; each Linux/macOS job records
47 discovered, 45 passed and two skips. These are results for that commit,
not CI of this uncommitted publication candidate. Fresh remote readback and
full historical log inspection are NOT_RUN in this local preparation.

CI success only proves the documented tests executed in that environment.
No complete functional platform acceptance, defect freedom, sandbox security
or production readiness is claimed. Host trust, directory protection, race
limitations, unsigned audit digests and unscreened text content remain explicit
limits. See [the threat model](docs/THREAT_MODEL.md).

Version 0.1.0 alone does not identify release bytes. Only the exact candidate
source/archive/wheel hash bindings may be considered for a future approval.
This is an unreleased draft: confidential security intake, final rights/name
review and remote publication evidence still have open prerequisites.

## Publication preparation and distinct owner gates

1. Confirm the exact source, public attribution and applicable third-party
   licenses. A brand designation does not establish a legal entity or prove
   the rights chain. Keep confidential personal identity records out of source,
   diffs, logs and release assets.
2. Verify an existing reachable confidential security reporting channel and
   responsible recipient, then document the confirmed route in SECURITY.md.
   Do not invent an address or send an unapproved test message.
3. Review all publishable history, full historical Actions logs and artifacts.
   Local excerpts cannot establish that remote publication content is safe.
4. Any commit/push of this local candidate requires a separate exact approval.
   Earlier consumed gates do not authorize it. No force push or CI rerun is
   implied. Verify the resulting remote commit/tree and configured nine jobs;
   their success applies only to the executed tests of that exact commit.
5. Rebuild and bind assets to the final source. Request Gate B only after all
   prerequisites are satisfied, specifying visibility, tag/release, exact
   assets and readback actions. No publication is authorized by this document.
6. GitHub private vulnerability reporting may be enabled after an explicitly
   authorized public visibility change, only if separately included in that
   authorization. Verify it before release; the preverified confidential
   contact must already exist. Stop on failure.

No deployment, production installation or personal identity disclosure is
part of this reference publication. FORGE_READY != EXECUTION_AUTHORIZED.
