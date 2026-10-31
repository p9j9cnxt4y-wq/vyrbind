"""Deterministic policy. No model, prompt, network, or automatic approval path."""
from __future__ import annotations

from dataclasses import dataclass
from .models import ContractError, Intent, RunContract, target_key

_LOCAL_OPERATION = "artifact.create_text"
_CONTROLLED_EFFECTS = frozenset({
    "network.connect", "upload.send", "deploy.apply", "runtime.activate",
    "secret.use", "permission.escalate", "memory.promote", "claim.promote",
    "artifact.overwrite", "artifact.delete", "tool.install", "current.switch",
})


@dataclass(frozen=True, slots=True)
class Verdict:
    status: str
    code: str


def evaluate(intent: Intent, contract: RunContract) -> Verdict:
    """Only new local text artifacts can be allowed; no delegated authorities."""
    if intent.scope_id != contract.scope_id or intent.run_id != contract.run_id:
        return Verdict("DENIED", "BOUND_SCOPE_MISMATCH")
    if intent.operation in _CONTROLLED_EFFECTS:
        # This is NOT an approval. No remote/approval executor ships in v0.1.
        return Verdict("HUMAN_GATE_REQUIRED", "NO_EXECUTOR_FOR_CONTROLLED_EFFECT")
    if intent.operation != _LOCAL_OPERATION:
        return Verdict("DENIED", "UNKNOWN_OPERATION")
    if intent.content == "":
        return Verdict("DENIED", "EMPTY_CONTENT")
    try:
        target_key(intent.target)
    except ContractError:
        return Verdict("DENIED", "OUT_OF_SCOPE_TARGET")
    return Verdict("ALLOWED_LOCAL", "BOUND_LOCAL_CREATE")
