"""Operator-side command entry point. NEVER expose arbitrary CLI args to a model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import ContractError, EvidenceLedger, IntegrityError, Intent, LocalBroker, RunContract

_MAX_JSON_BYTES = 20_000


def _reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
    out = {}
    for key, value in pairs:
        if key in out:
            raise ContractError("DUPLICATE_JSON_KEY")
        out[key] = value
    return out


def parse_intent(path: Path) -> Intent:
    # Bounded read, not a check-then-unbounded-read of potentially changing data.
    with path.open("rb") as handle:
        raw = handle.read(_MAX_JSON_BYTES + 1)
    if len(raw) > _MAX_JSON_BYTES:
        raise ContractError("OVERSIZED_JSON")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates,
                          parse_constant=lambda _: (_ for _ in ()).throw(ContractError("INVALID_JSON_NUMBER")))
    except (ValueError, UnicodeError, RecursionError) as exc:
        if isinstance(exc, ContractError):
            raise
        raise ContractError("INVALID_JSON") from exc
    return Intent.from_mapping(data)


def _print(result: dict) -> None:
    print(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="forgeproofgate", description="Local-only deterministic AI action gate")
    subs = parser.add_subparsers(dest="command", required=True)
    run = subs.add_parser("run", help="Controlled local create from an untrusted intent JSON")
    run.add_argument("--workspace", type=Path, required=True, help="Operator-bound, existing EMPTY output folder")
    run.add_argument("--audit-db", type=Path, required=True, help="Evidence DB outside workspace")
    run.add_argument("--scope", required=True)
    run.add_argument("--run-id", required=True)
    run.add_argument("--intent", type=Path, required=True)
    verify = subs.add_parser("verify", help="Verify the local evidence hash chain")
    verify.add_argument("--audit-db", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "verify":
            ledger = EvidenceLedger(args.audit_db.absolute(), readonly=True)
            try:
                count, head = ledger.head()
            finally:
                ledger.close()
            _print({"status": "PASS_CHAIN_ONLY", "event_count": count, "head_sha256": head})
            return 0
        intent = parse_intent(args.intent)
        contract = RunContract(scope_id=args.scope, run_id=args.run_id,
                               workspace=args.workspace.absolute(), audit_db=args.audit_db.absolute())
        with LocalBroker(contract) as broker:
            result = broker.invoke(intent)
        _print(result.as_dict())
        return 0 if result.status == "PASS_LOCAL_EFFECT" else 2
    except (ContractError, IntegrityError, OSError) as exc:
        # Never print paths, user-supplied data, or underlying system errors.
        code = str(exc) if isinstance(exc, (ContractError, IntegrityError)) else "IO_FAILURE"
        if code not in {"INVALID_SCHEMA", "INVALID_RUN_ID", "INVALID_SCOPE_ID", "INVALID_ACTION_ID",
                        "INVALID_OPERATION", "INVALID_TARGET", "INVALID_CONTENT", "INVALID_JSON",
                        "INVALID_JSON_NUMBER", "DUPLICATE_JSON_KEY", "OVERSIZED_JSON",
                        "UNTRUSTED_WORKSPACE", "WORKSPACE_CHANGED", "WORKSPACE_NOT_AVAILABLE",
                        "AUDIT_INSIDE_WORKSPACE", "UNTRUSTED_AUDIT_PARENT", "AUDIT_LOCKED_OPERATOR_RECOVERY_REQUIRED",
                        "AUDIT_LOCK_FAILED", "INVALID_AUDIT_LOCATION", "INVALID_AUDIT_FILE", "NO_AUDIT_FILE",
                        "AUDIT_READ_FAILED", "AUDIT_LIMIT_REACHED", "AUDIT_CHAIN_INVALID", "AUDIT_FIELDS_INVALID",
                        "AUDIT_HASH_MISMATCH", "INVALID_AUDIT_EVENT", "AUDIT_READ_ONLY", "AUDIT_APPEND_FAILED",
                        "DUPLICATE_ACTION_RECORD", "UNMATCHED_EFFECT_RECORD", "DUPLICATE_TARGET_RECORD",
                        "UNKNOWN_EFFECT_OPERATOR_READBACK_REQUIRED", "UNFINISHED_EFFECT_OPERATOR_READBACK_REQUIRED",
                        "UNTRACKED_NODE_IN_WORKSPACE", "UNTRACKED_ARTIFACT", "ARTIFACT_SIZE_CHANGED",
                        "ARTIFACT_DIGEST_MISMATCH", "READBACK_FAILED", "MISSING_ARTIFACT", "BROKER_NOT_OPEN",
                        "BROKER_ALREADY_OPEN", "READBACK_DIGEST_MISMATCH", "AUDIT_RACE", "RUN_CONTRACT_MISMATCH", "AUDIT_OPEN_FAILED"}:
            code = "BLOCKED_INTERNAL"
        _print({"status": "BLOCKED", "code": code})
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
