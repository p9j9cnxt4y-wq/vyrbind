# Proposed publication metadata

**Repository name:** `forgeproofgate` (provisional; no trademark clearance)  
**Title:** ForgeProofGate — Deterministic Safety Boundary for AI Agents  
**Short description:** A dependency-free Python reference for fail-closed agent tool authorization, bounded local artifact writes, and verifiable readback evidence.  
**Topics:** `ai-agents`, `agent-security`, `policy-engine`, `least-privilege`, `fail-closed`, `python`, `safety-invariants`

## Suggested first-release note

ForgeProofGate v0.1.0 demonstrates how a limited set of AI-agent safety invariants
can be enforced in ordinary Python code rather than relying on a system
prompt. It rejects unknown tools and out-of-scope actions, allows only new
text artifacts within a pre-bound local workspace, verifies actual effects,
and writes hash-linked audit records. All other effects, including deployment,
network, credentials, and training, remain disabled.

The release is a **local reference implementation**, not an audited firewall,
zero-knowledge system, human-approval service, or production-ready AI agent.

## Manual publisher steps

1. Confirm legal publisher attribution, repository name and MIT license.
2. Enable private vulnerability reporting and replace the note in SECURITY.md.
3. Check the CI matrix passes against the exact release commit.
4. Confirm release archive and wheel digests independently.
5. Publish only after an explicit operator decision; do not auto-deploy or
   connect production systems as part of this reference release.
