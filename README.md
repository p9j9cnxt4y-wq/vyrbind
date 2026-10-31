# ForgeProofGate

Project and publisher brand: **vYronFORGE.**

Copyright (c) 2026 vYronFORGE.

Independent engineering reference. Not an OpenAI product or an OS sandbox.
The public attribution is a brand designation and does not assert a legal form.

**A deterministic, fail-closed reference boundary for tool-using AI agents.**

[Deutsche Anleitung](README.de.md) · [Threat model](docs/THREAT_MODEL.md) · [Invariant coverage](docs/INVARIANTS.md)

> **Status: unreleased v0.1.0 candidate / local-only reference / not security-certified.**
> This package is not an OS sandbox, a replacement for access control, an authenticated
> human-approval system, an independent truth engine, or a protection layer for arbitrary
> agent tools. **Do not give an AI agent access to this package's operator CLI arguments,
> the Python host process, policy construction, audit store, or workspace parent.**

## Implemented behavior and test scope

- Strict validation of untrusted JSON intent: exact schema, bounded size, duplicate-key rejection, restricted child filenames.
- Trusted operator contract binds **run, scope, workspace and separate evidence store**.
- **One real local effect**: create a NEW UTF-8 `.txt` file, never overwrite it.
- All unknown tools and operations are denied; controlled effects return `HUMAN_GATE_REQUIRED` but have **no executor** in this version.
- The package's runtime executor has no network, shell, deletion, secret reading, model inference, memory promotion or deployment operation. Tests create and clean up synthetic fixtures; Windows junction tests use the local `mklink` command.
- SQLite-based digest-only evidence chain with readback, corruption checks, unique action IDs and recovery stop states.
- Invariant checks before the action and a separate artifact readback afterward.
- A dependency-free Python runtime declaring Python 3.11+; this minimum version is not evidence that every interpreter/platform combination has been tested.

Windows checks cover targeted code, unit, regression, negative and smoke behavior
in the tested scope; they are **not a complete functional product acceptance**.
The local source suite on Python 3.12.10, 3.13.13 and 3.15.0 discovers 47 tests:
46 pass and one is skipped per run because the fixture volume does not support
distinct case-sensitive sibling names. The smoke scripts exit 0. See
[exact results and historical CI](RELEASE_EVIDENCE.md).

The retained CI record for commit
`1e781555e7ff6ab6a93c97146aa3136c3ade4ff0`, run `41203391771`, reports nine
successful jobs (Windows, Linux and macOS; Python 3.11/3.12/3.13). This local
publication candidate changes attribution and documentation only; its runtime,
tests and workflow match that commit. The candidate has no new commit or CI
run. Fresh remote readback and complete historical log review remain NOT_RUN
in this local preparation. A GitHub Actions PASS means
only that the documented tests passed for that specific commit and environment.
It does not establish general freedom from defects, complete sandbox security,
production readiness or guaranteed cross-platform compatibility.

## Quick start (offline, standard library only)

```sh
python tools/verify.py
python tools/smoke.py
```

Optional installation requires setuptools >=77 and may download build tooling
unless it is already available. For an offline installation with that tooling
present:

```sh
python -m pip install --no-index --no-deps --no-build-isolation -e .
forgeproofgate --help
```

Run the following POSIX-shell sample **from an operator-controlled shell**, not
from an agent. The Python verification scripts above also run from PowerShell;
the POSIX shell syntax below is not a Windows compatibility claim:

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
    workspace=Path("./controlled-output").absolute(),
    audit_db=Path("./protected-evidence/events.sqlite").absolute(),
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
Pass the original absolute paths; do not resolve away direct workspace or audit
links before the broker can inspect them. Trusted ancestor aliases are handled
by physical containment checks, not by granting trust to arbitrary links.

## Implemented scope and limits

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

No verified confidential security reporting contact is available yet. Public
release remains blocked until one is documented; see [SECURITY.md](SECURITY.md).
Do not submit vulnerability details or sensitive data to public issues.
The current candidate has no new commit, push or CI authorization. Draft release
notes and the separate publication gates are in [PUBLISHING.md](PUBLISHING.md).
