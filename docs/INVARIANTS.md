# Invariant mapping — research principles to code (v0.1.0)

The research base distinguishes **capability**, **authority**, **evidence** and
**effect**. The following table is an implementation coverage statement, not
an assertion that all 30 research invariants are enforced everywhere.

`TESTED_LOCAL` and `TESTED_LOCAL_SCOPE` refer only to the targeted Windows
code/unit/regression/negative/smoke checks described in
[the current verification record](../RELEASE_EVIDENCE.md), including its skips.
They do not mean complete functional product acceptance or a verified Linux/
macOS correction. GitHub Actions PASS covers only documented tests of that
specific commit/environment, not all invariants, general freedom from defects,
complete sandbox security, production readiness or guaranteed compatibility.

| Principle | Concrete enforcement in this package | Status |
| --- | --- | --- |
| Prompt != Policy | Model text is never evaluated as configuration; exact intents only | TESTED_LOCAL |
| Content != Authority | File content never passed to policy or executed | TESTED_LOCAL |
| Reachable != Authorized | No network or arbitrary tool adapters exist | TESTED_LOCAL_SCOPE |
| Model output = untrusted input | Strict keys/types/size + deterministic evaluator | TESTED_LOCAL |
| Human ID != Agent ID | No identity delegation; host identity external | NOT_IMPLEMENTED_HOST_BOUNDARY |
| Eval != Production | No remote/production adapters | TESTED_LOCAL_SCOPE |
| Subagent authority cannot amplify | No subagents or delegation | NOT_APPLICABLE_NO_SUBAGENTS |
| No evidence => no PASS | Readback + evidence append + postcondition check | TESTED_LOCAL |
| Containment failure => fail | Scope/target/ledger checks stop broker | TESTED_LOCAL_SCOPE |
| Unknown target => deny | Single valid child filename, no path navigation | TESTED_LOCAL |
| Unknown tool => deny | Single allowlisted operation | TESTED_LOCAL |
| Monitoring failure => abort | Missing/mutated evidence blocks subsequent run | TESTED_LOCAL_LEDGER |
| Secret access => broker-only | Secret reading not implemented | DENIED_NO_SECRET_BROKER |
| External effect => operator gate | `HUMAN_GATE_REQUIRED`, no executor | DENIED_BY_DESIGN |
| Policy outside model control | Host supplies contract, no model policy tool | REQUIRES_HOST_ISOLATION |
| Verify containment before outcome | Scope, file and chain checked before execute | TESTED_LOCAL |
| Upload != deploy != runtime | All absent/blocked | DENIED_BY_DESIGN |
| Local work != remote authority | No remote operations | DENIED_BY_DESIGN |
| Memory promotion explicit | Memory promotion has no executor | DENIED_BY_DESIGN |
| Evidence append-only/hash-linked | SQLite append API, linked digests | TESTED_LOCAL_NOT_TAMPER_PROOF |
| Capabilities explicit/non-delegable | Only `artifact.create_text` exposed | TESTED_LOCAL_SCOPE |
| Environment contradiction => deny | Changed root / unexpected file / changed run | TESTED_LOCAL_SCOPE |
| No public registry writes during eval | No publication code | DENIED_BY_DESIGN |
| No product authority collapse | Not integrated with any other product | NOT_APPLICABLE_STANDALONE |
| Research review has no effect authority | No research reviewer can execute | DENIED_BY_DESIGN |
| Machine review != human approval | No machine-issued human grant | DENIED_BY_DESIGN |
| Cleanup and revocation verified | No external creds/sessions; crash lock needs operator recovery | PARTIAL_NO_REVOCATION_BACKEND |
| Sensitive values redacted | Audit stores digests only, output content NOT scrubbed | PARTIAL |
| One run / one bound scope | Contract-binding evidence and scope match | TESTED_LOCAL |
| Human can stop | Host process may be stopped; no independent kill switch | NOT_IMPLEMENTED |

**Research policy vs code:** Falsification, independent source verification,
claim provenance, memory truth promotion, multi-agent review and human
coexistence are crucial design principles but require external independent
verifiers. This package deliberately **denies** their effects instead of
pretending to implement them.
