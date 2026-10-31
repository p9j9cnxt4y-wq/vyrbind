"""Public, data-only action intent and non-forgeable-by-text run contracts.

The trusted host MUST construct RunContract separately from model output. Python
objects are not an OS security boundary; see docs/THREAT_MODEL.md.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

MAX_CONTENT_BYTES = 16_384
_IDENT = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,79}$", re.ASCII)
_TARGET = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,59}\.txt$", re.ASCII | re.IGNORECASE)
_RESERVED_WINDOWS = frozenset({"CON", "PRN", "AUX", "NUL", *(f"COM{x}" for x in range(1, 10)), *(f"LPT{x}" for x in range(1, 10))})


class ContractError(ValueError):
    """Malformed caller-controlled input or invalid operator contract."""


def _identifier(value: object, key: str) -> str:
    if not isinstance(value, str) or not _IDENT.fullmatch(value):
        raise ContractError(f"INVALID_{key.upper()}")
    return value


def target_key(filename: str) -> str:
    """Normalize ONLY a single child filename; no paths are ever allowed."""
    if not isinstance(filename, str) or not _TARGET.fullmatch(filename):
        raise ContractError("INVALID_TARGET")
    if ".." in filename or filename.split(".")[0].upper() in _RESERVED_WINDOWS:
        raise ContractError("INVALID_TARGET")
    return filename.casefold()


@dataclass(frozen=True, slots=True)
class Intent:
    run_id: str
    scope_id: str
    action_id: str
    operation: str
    target: str
    content: str

    def __post_init__(self) -> None:
        _identifier(self.run_id, "run_id")
        _identifier(self.scope_id, "scope_id")
        _identifier(self.action_id, "action_id")
        _identifier(self.operation, "operation")
        if not isinstance(self.target, str) or len(self.target) > 1000:
            raise ContractError("INVALID_TARGET")
        try:
            self.target.encode("utf-8")
        except UnicodeError as exc:
            raise ContractError("INVALID_TARGET") from exc
        if not isinstance(self.content, str) or "\x00" in self.content:
            raise ContractError("INVALID_CONTENT")
        try:
            size = len(self.content.encode("utf-8"))
        except UnicodeError as exc:
            raise ContractError("INVALID_CONTENT") from exc
        if size > MAX_CONTENT_BYTES:
            raise ContractError("INVALID_CONTENT")

    @classmethod
    def from_mapping(cls, data: object) -> "Intent":
        # Reject unknown fields: future fields must receive explicit review.
        keys = {"run_id", "scope_id", "action_id", "operation", "target", "content"}
        if not isinstance(data, dict) or set(data) != keys:
            raise ContractError("INVALID_SCHEMA")
        run_id = _identifier(data["run_id"], "run_id")
        scope_id = _identifier(data["scope_id"], "scope_id")
        action_id = _identifier(data["action_id"], "action_id")
        operation = _identifier(data["operation"], "operation")
        return cls(run_id, scope_id, action_id, operation,
                   data["target"], data["content"])


@dataclass(frozen=True, slots=True)
class RunContract:
    """Operator-controlled binding. NEVER build this from model text."""
    scope_id: str
    run_id: str
    workspace: Path
    audit_db: Path

    def __post_init__(self) -> None:
        _identifier(self.scope_id, "scope_id")
        _identifier(self.run_id, "run_id")
        if (not isinstance(self.workspace, Path) or not isinstance(self.audit_db, Path)
                or not self.workspace.is_absolute() or not self.audit_db.is_absolute()):
            raise ContractError("INVALID_PATH_BINDING")


@dataclass(frozen=True, slots=True)
class Result:
    status: str
    code: str
    receipt_hash: str | None = None

    def as_dict(self) -> dict[str, str | None]:
        return {"status": self.status, "code": self.code, "receipt_hash": self.receipt_hash}
