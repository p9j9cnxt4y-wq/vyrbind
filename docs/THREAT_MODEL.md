# Security model / boundaries / residual risks

## Trust boundary

The trusted host controls `RunContract`, executable code, the process identity,
workspace parent directory and audit-directory ownership. Everything originating
with a model (including the JSON intent, filename and content) is untrusted **data**.
The model cannot have arbitrary Python, shell, operating-system or filesystem
access. Giving it those capabilities defeats this package.

ForgeProofGate is a local *broker*, not an operating-system access-control
mechanism. If an attacker can call the broker's constructor or mutate the
trusted host, choose a different policy, change source code, create hardlinks,
replace parent directories, or edit SQLite directly, the library cannot stop it.

## Explicit scope of this implementation

- One effect: exclusive creation of a direct-child UTF-8 `.txt` artifact.
- No recursive paths, symlink workspaces, overwrite, delete or shell execution.
- Separate audit location; simple exclusive lock file for single broker use.
- Before lock/ledger creation, audit-parent ancestry is compared by physical
  directory identity with the bound workspace. Trusted ancestor aliases and
  `..` are not accepted as a way to place an audit file inside the workspace.
  Original I/O paths and direct workspace/audit link checks remain in place.
- Scope and run ID fixed by trusted caller, recorded by hashed contract binding.
- Reject unknown operations, extra JSON fields, duplicate JSON keys, malformed
  content, reserved filenames and content exceeding 16,384 UTF-8 bytes.
- No automatic retry if an effect is uncertain.
- No network client, HTTP fetch, installer, secret store, remote runtime or
  approval receipt generator exists in the package.

## Attack scenarios and expected behavior

| Attack | Intended response | Test |
| --- | --- | --- |
| Prompt asks to deploy or elevate access | `HUMAN_GATE_REQUIRED`, never executes | test_deploy_requires_human_gate_and_never_executes |
| Tool name unknown | `UNKNOWN_OPERATION` | test_unknown_tool_denied |
| Target path traversal or reserved filename | `OUT_OF_SCOPE_TARGET` | test_traversal_blocked |
| Different run/scope | `BOUND_SCOPE_MISMATCH` | test_scope_mismatch_denied |
| Duplicate action ID | `REPLAYED_ACTION_ID` | test_replay_action_id_is_blocked |
| Existing file overwritten | Exclusive create prevents overwrite | test_duplicate_target_is_not_overwritten |
| Tampered event row | Fail closed on hash mismatch | test_tampered_audit_chain_blocks_run |
| Changed or untracked artifact | Fail closed on readback | test_modified_artifact_blocks_next_action |
| Crash after allow / unresolved effect | Stop; operator readback required | test_unfinished_effect_after_crash_blocks_reuse |
| Raw injection string in content | Literal file content, not executed | test_content_is_inert_data_not_instruction |
| Audit file inside workspace via ancestor alias or `..` | `AUDIT_INSIDE_WORKSPACE` before lock/ledger creation | test_both_paths_under_alias_inside_are_rejected; test_dotdot_inside_is_rejected_before_writes |
| Valid external audit through trusted ancestor alias | Bounded text creation and audit readback | test_alias_sibling_audit_allows_verified_effect |

## Verification limits

Current Windows checks are targeted code, unit, regression, negative and smoke
checks, not complete functional product acceptance. A case-sensitive sibling
test is skipped on the tested case-insensitive fixture volume. New corrections
are functionally unconfirmed on Linux/macOS; historical Linux success belongs
only to its recorded commit. See [RELEASE_EVIDENCE.md](../RELEASE_EVIDENCE.md).
GitHub Actions PASS means only the documented tests of that commit/environment
passed. It cannot establish general defect freedom, full sandbox safety,
production readiness or guaranteed cross-platform compatibility.

The physical parent check does not make ancestor changes race-free, authenticate
host trust or guarantee error priority for every invalid directory-valued audit
path. Those invalid-path edge cases are not promoted to tested platform coverage.

## Known gaps: must not be represented as covered

1. **No OS isolation.** Filename validation and pre/post directory checks cannot
   prevent root-substitution races by a hostile actor with directory permissions.
   Even a permitted local write could be redirected by a privileged concurrent
   filesystem attacker. Production use needs a dedicated sandbox/ACLs and,
   where supported, descriptor-relative operations secured against races.
2. **No authenticated human approval.** The marker `HUMAN_GATE_REQUIRED` is not
   an accepted approval. There is no grant issuer, approval verifier or external
   execution adapter. A future gate needs dedicated identity, scope, expiry,
   nonce, one-time consumption, denial on replay, audit and revocation.
3. **Audit hashes are not signatures.** A writer able to rewrite all rows can
   recompute the hash chain, truncate it or replace the DB. The chain alone
   does not prove integrity against a powerful adversary. Publish each final
   head digest to an independently protected store and enforce storage ACLs.
4. **No durable external transaction.** Filesystem writes and SQLite commits
   are not atomic across both stores. A process interruption after writing a
   file but before `EFFECT_OK` leaves an orphan/pending record and blocks reuse.
   Manually reconcile after readback. Automatic cleanup/replay is forbidden.
5. **No secret detection or ZK proof.** Audit avoids plaintext, but the
   approved artifact writes input content verbatim. Sensitive content may leak
   if the workspace is readable to others. Hashes can allow dictionary attacks.
6. **No objective epistemic checker.** Evidence is provided only for the
   broker's local effects. `claim.promote` and `memory.promote` cannot run.
   Proper research truth promotion requires independently trusted sources and
   falsification procedures outside model control.
7. **No multi-tenant support.** Locking is single-run and fail-closed. OS users,
   group permissions, ACLs and service accounts must be isolated separately.
8. **No resource-general denial-of-service defense.** Input and ledger limits
   exist, but an attacker able to issue unlimited calls can exhaust local disk.
   An external service would require quotas, rate limiting and monitoring.

## No-automatic-recovery policy

`BLOCKED_UNCERTAIN_EFFECT`/`UNKNOWN_EFFECT_OPERATOR_READBACK_REQUIRED` are
terminal safety stops. Do not delete/rebuild the ledger, edit a result into
`PASS`, or retry blindly. An authorized operator must inspect effects and
establish a new trusted baseline, preserving original evidence.

## Publication checklist

- [ ] Author/maintainer/license verified
- [ ] Name and trademarks checked before branding
- [ ] Host permissions and deployment assumptions documented
- [ ] Cross-platform CI passing on the release commit
- [ ] Threat model and known limitations accepted
- [ ] Independent security review for any production use
- [ ] Private vulnerability reporting channel configured
- [ ] No secrets, real paths, private identifiers or company infrastructure in release
