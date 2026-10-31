# ForgeProofGate

Independent vYronFORGE engineering reference. Not an OpenAI product or an OS sandbox.

**A deterministic, fail-closed reference boundary for tool-using AI agents.**

[Deutsche Anleitung](README.de.md) · [Threat model](docs/THREAT_MODEL.md) · [Invariant coverage](docs/INVARIANTS.md)

> **Status: v0.1.0 / local-only reference implementation / not security-certified.**
> This package is not an OS sandbox, a replacement for access control, an authenticated
> human-approval system, an independent truth engine, or a protection layer for arbitrary
> agent tools. **Do not give an AI agent access to this package's operator CLI arguments,
> the Python host process, policy construction, audit store, or workspace parent.**

## What works

- Strict validation of untrusted JSON intent: exact schema, bounded size, duplicate-key rejection, restricted child filenames.
- Trusted operator contract binds **run, scope, workspace and separate evidence store**.
- **One real local effect**: create a NEW UTF-8 `.txt` file, never overwrite it.
- All unknown tools and operations are denied; controlled effects return `HUMAN_GATE_REQUIRED` but have **no executor** in this version.
- No network, shell, deletion, secret reading, model inference, memory promotion or deployment code.
- SQLite-based digest-only evidence chain with readback, corruption checks, unique action IDs and recovery stop states.
- Invariant checks before the action and a separate artifact readback afterward.
- A small, dependency-free Python runtime (Python 3.11+), with tests and a local smoke script.

## Quick start (offline, standard library only)

```sh
python tools/verify.py
python tools/smoke.py
```

Optionally install as a Python package (setuptools is needed only to build/install):

```sh
python -m pip install -e .
forgeproofgate --help
```

Run the static sample **from an operator-controlled shell**, not from an agent:

```sh
mkdir -p ./local-run/workspace ./local-run/evidence
PYTHONPATH=src python -m forgeproofgate.cli run \
  --workspace ./local-run/workspace \
  --audit-db ./local-run/evidence/events.sqlite \
  --scope local-publication --run-id publication-run-001 \
  --intent examples/allow.json

PYTHONPATH=src python -m forgeproofgate.cli verify \
  --audit-db ./local-run/evidence/events.sqlite
```

The `run` command creates `local-run/workspace/hello.txt`. The `verify` command
verifies the **internal hash chain only**; it does not authenticate a publisher,
validate the workspace contents or prove anything about the host environment.

A second request for the same action ID is denied. An untracked file, mutated
output, bad chain or unresolved effect blocks subsequent runs until a human
investigates. Do **not** delete a lock file or reset evidence just to continue.
Use a fresh local-run directory for the example each time.

## Integration contract

```python
from pathlib import Path
from forgeproofgate import Intent, LocalBroker, RunContract

# Trusted host creates this. NEVER accept these paths or IDs from model output.
contract = RunContract(
    scope_id="fixed-scope",
    run_id="operator-run-001",
    workspace=Path("./controlled-output").resolve(),
    audit_db=Path("./protected-evidence/events.sqlite").resolve(),
)

# The folders already exist; the workspace must initially be empty.
# This is *data from the model*, not a policy or an approval.
intent = Intent.from_mapping({
    "run_id": "operator-run-001", "scope_id": "fixed-scope",
    "action_id": "request-001", "operation": "artifact.create_text",
    "target": "result.txt", "content": "Research note, not an instruction.\n",
})
with LocalBroker(contract) as broker:
    result = broker.invoke(intent)
print(result.as_dict())
```

The trusted host must prepare/protect the directories, own the Python runtime,
and supply a binding that an agent cannot modify. This package **does not** make
those conditions true by itself.

## Scope and guarantees

| Feature | v0.1.0 |
| --- | --- |
| Strict action parsing and fail-closed local tool allowlist | Implemented and locally tested |
| Exclusive local `.txt` creation + digest readback | Implemented and locally tested |
| Existing artifact and audit consistency checks | Implemented and locally tested |
| Hash-linked audit chain | Implemented; **not externally authenticated** |
| Human gate for upload/deploy/remote mutation | Blocked by design; issuer/executor **not implemented** |
| Memory/claim promotion with independent epistemic proof | Blocked; **not implemented** |
| Secrets/identity broker, OS isolation, external egress enforcement | **Not implemented** |
| Secure multi-tenant or remotely deployed use | **Not supported** |
| Universal prompt-injection defense | **Not claimed** |

The code converts a subset of AI safety research principles into observable
engineering constraints: `MODEL_OUTPUT != POLICY`, `CAPABILITY != AUTHORITY`,
`NO_EVIDENCE => NO_PASS`, `UNKNOWN => DENY`, `EFFECT_UNKNOWN => STOP`,
and `EVIDENCE != APPROVAL`. It does not claim that these principles have been
universally proven or that a successful local regression is a production proof.

## Threat and privacy notes

Model-supplied `content` is written **verbatim** to the explicitly approved
workspace file; it is not interpreted as instructions by ForgeProofGate. The
system does **not** reliably detect secrets in file content, and should only be
given data approved for that workspace. The evidence database stores digests
and fixed status codes, not text content, URLs or raw target names. Digests
can still reveal information through guessing attacks; do not treat them as
Zero-Knowledge proofs. Host access controls remain mandatory.

For root path replacement, hostile filesystem actors, untrusted multi-user
machines or remotely accessible services, a dedicated operating-system sandbox
and separate trust principals are required; this reference does not supply them.
See [the threat model](docs/THREAT_MODEL.md).

## License and publication

MIT License — see [LICENSE](LICENSE). Project name is provisional, not a
trademark clearance. No repository, deployment, cloud service or account
changes are made by this package. The test suite uses only local temporary
files and SQLite databases.

A security report should be sent privately using the disclosure mechanism the
repository maintainer configures before public release; see [SECURITY.md](SECURITY.md).
