"""One safe effect: create a new UTF-8 text file in a pre-bound workspace.

NO: shell, networking, deletion, overwrite, secrets, deployment, or training.
The broker requires a trusted host + OS confinement. See THREAT_MODEL.md.
"""
from __future__ import annotations

import os
from pathlib import Path
import stat

from .evidence import EvidenceLedger, IntegrityError, digest, sha256
from .models import MAX_CONTENT_BYTES, ContractError, Intent, Result, RunContract, target_key
from .policy import evaluate


class LocalBroker:
    """Single-host-run broker with exclusive crash-visible lock and readback."""

    def __init__(self, contract: RunContract) -> None:
        self.contract = contract
        self._ledger: EvidenceLedger | None = None
        self._lock_fd: int | None = None
        self._entered = False
        self._root_resolved: Path | None = None
        self._root_identity: tuple[int, int] | None = None

    def _check_root(self) -> None:
        root = self.contract.workspace
        try:
            node = root.lstat()
            resolved = root.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise IntegrityError("WORKSPACE_NOT_AVAILABLE") from exc
        reparse_point = bool(
            getattr(node, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        )
        if (not stat.S_ISDIR(node.st_mode) or root.is_symlink() or reparse_point
                or (hasattr(root, "is_junction") and root.is_junction())):
            raise IntegrityError("UNTRUSTED_WORKSPACE")
        if self._root_resolved is not None and (
            resolved != self._root_resolved or
            (node.st_dev, node.st_ino) != self._root_identity
        ):
            raise IntegrityError("WORKSPACE_CHANGED")

    def __enter__(self) -> "LocalBroker":
        if self._entered:
            raise IntegrityError("BROKER_ALREADY_OPEN")
        self._check_root()
        self._root_resolved = self.contract.workspace.resolve(strict=True)
        node = self.contract.workspace.lstat()
        self._root_identity = (node.st_dev, node.st_ino)
        # State and workspace must be separate. No evidence writes into agent outputs.
        state = self.contract.audit_db.absolute()
        root = self._root_resolved
        if not state.is_absolute() or state == root or root in state.parents:
            raise IntegrityError("AUDIT_INSIDE_WORKSPACE")
        if not state.parent.is_dir() or state.parent.is_symlink():
            raise IntegrityError("UNTRUSTED_AUDIT_PARENT")
        lock = state.with_name(state.name + ".lock")
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        if hasattr(os, "O_BINARY"):
            flags |= os.O_BINARY
        try:
            self._lock_fd = os.open(lock, flags, 0o600)
        except FileExistsError:
            raise IntegrityError("AUDIT_LOCKED_OPERATOR_RECOVERY_REQUIRED") from None
        except OSError as exc:
            raise IntegrityError("AUDIT_LOCK_FAILED") from exc
        try:
            self._ledger = EvidenceLedger(state)
            if not self._ledger.events():
                self._ledger.append(
                    phase="CONTRACT_BIND", action_hash=digest(self.contract.run_id),
                    target_hash=digest(self.contract.scope_id), content_hash=digest(str(root)),
                    code="RUN_SCOPE_BOUND",
                )
            self._reconcile(self._ledger.events())
        except BaseException:
            self.__exit__(None, None, None)
            raise
        self._entered = True
        return self

    def __exit__(self, *_: object) -> None:
        if self._ledger is not None:
            self._ledger.close()
            self._ledger = None
        if self._lock_fd is not None:
            os.close(self._lock_fd)
            self._lock_fd = None
            self.contract.audit_db.absolute().with_name(self.contract.audit_db.name + ".lock").unlink(missing_ok=True)
        self._entered = False

    def _reconcile(self, events: list) -> None:
        """Any orphan file, altered artifact, or pending effect blocks the next run."""
        self._check_root()
        if (not events or events[0].phase != "CONTRACT_BIND" or
                events[0].action_hash != digest(self.contract.run_id) or
                events[0].target_hash != digest(self.contract.scope_id) or
                events[0].content_hash != digest(str(self._root_resolved)) or
                any(event.phase == "CONTRACT_BIND" for event in events[1:])):
            raise IntegrityError("RUN_CONTRACT_MISMATCH")
        expected: dict[str, str] = {}
        pending: dict[str, tuple[str, str]] = {}
        for event in events[1:]:
            key = event.action_hash
            if event.phase == "DECISION_ALLOW":
                if key in pending:
                    raise IntegrityError("DUPLICATE_ACTION_RECORD")
                pending[key] = (event.target_hash, event.content_hash)
            elif event.phase == "EFFECT_OK":
                if key not in pending or pending[key] != (event.target_hash, event.content_hash):
                    raise IntegrityError("UNMATCHED_EFFECT_RECORD")
                if event.target_hash in expected:
                    raise IntegrityError("DUPLICATE_TARGET_RECORD")
                expected[event.target_hash] = event.content_hash
                del pending[key]
            elif event.phase == "EFFECT_UNKNOWN":
                raise IntegrityError("UNKNOWN_EFFECT_OPERATOR_READBACK_REQUIRED")
        if pending:
            raise IntegrityError("UNFINISHED_EFFECT_OPERATOR_READBACK_REQUIRED")
        present: dict[str, str] = {}
        try:
            for node in self.contract.workspace.iterdir():
                if node.is_symlink() or not node.is_file():
                    raise IntegrityError("UNTRACKED_NODE_IN_WORKSPACE")
                try:
                    target_key(node.name)
                except ContractError as exc:
                    raise IntegrityError("UNTRACKED_NODE_IN_WORKSPACE") from exc
                target_digest = digest(node.name.casefold())
                if target_digest in present or target_digest not in expected:
                    raise IntegrityError("UNTRACKED_ARTIFACT")
                # Verification is readback of files we own, no outside read.
                if node.stat().st_size > MAX_CONTENT_BYTES:
                    raise IntegrityError("ARTIFACT_SIZE_CHANGED")
                with node.open("rb") as handle:
                    content_digest = sha256(handle.read(MAX_CONTENT_BYTES + 1))
                if content_digest != expected[target_digest]:
                    raise IntegrityError("ARTIFACT_DIGEST_MISMATCH")
                present[target_digest] = content_digest
        except OSError as exc:
            raise IntegrityError("READBACK_FAILED") from exc
        if set(present) != set(expected):
            raise IntegrityError("MISSING_ARTIFACT")

    def _create(self, filename: str, payload: bytes) -> None:
        """Exclusive create only; external actors must not mutate the trusted root."""
        self._check_root()
        target_key(filename)
        path = self.contract.workspace / filename
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0)
        try:
            fd = os.open(path, flags, 0o600)
        except OSError:
            raise
        try:
            with os.fdopen(fd, "wb") as file:
                file.write(payload)
                file.flush()
                os.fsync(file.fileno())
            # Target cannot be a link because creation was exclusive.
            with path.open("rb") as check:
                actual = check.read(len(payload) + 1)
            if sha256(actual) != sha256(payload):
                raise IntegrityError("READBACK_DIGEST_MISMATCH")
        except Exception:
            # Never silently erase a possibly mutated/partial artifact.
            raise

    def invoke(self, intent: Intent) -> Result:
        if not self._entered or self._ledger is None:
            raise IntegrityError("BROKER_NOT_OPEN")
        if not isinstance(intent, Intent):
            raise ContractError("INVALID_SCHEMA")
        # Integrity verification precedes ANY policy decision or write.
        events = self._ledger.events()
        self._reconcile(events)
        action_hash = digest(intent.action_id)
        target_hash = digest(intent.target.casefold())
        content_hash = sha256(intent.content.encode("utf-8"))
        if any(event.phase in ("DECISION_ALLOW", "DECISION_DENY") and
               event.action_hash == action_hash for event in events):
            return Result("DENIED", "REPLAYED_ACTION_ID")
        verdict = evaluate(intent, self.contract)
        if verdict.status == "ALLOWED_LOCAL" and any(
            event.phase == "EFFECT_OK" and event.target_hash == target_hash
            for event in events
        ):
            verdict = type(verdict)("DENIED", "TARGET_ALREADY_EXISTS")
        if verdict.status != "ALLOWED_LOCAL":
            receipt = self._ledger.append(phase="DECISION_DENY", action_hash=action_hash,
                target_hash=target_hash, content_hash=content_hash, code=verdict.code)
            return Result(verdict.status, verdict.code, receipt)
        payload = intent.content.encode("utf-8")
        receipt = self._ledger.append(phase="DECISION_ALLOW", action_hash=action_hash,
            target_hash=target_hash, content_hash=content_hash, code=verdict.code)
        try:
            self._create(intent.target, payload)
        except (OSError, IntegrityError):
            # No implicit retry after a potentially partial effect.
            self._ledger.append(phase="EFFECT_UNKNOWN", action_hash=action_hash,
                target_hash=target_hash, content_hash=content_hash, code="READBACK_REQUIRED")
            return Result("BLOCKED_UNCERTAIN_EFFECT", "READBACK_REQUIRED", receipt)
        final_receipt = self._ledger.append(phase="EFFECT_OK", action_hash=action_hash,
            target_hash=target_hash, content_hash=content_hash, code="READBACK_PASS")
        # Postcondition check is independent of the earlier readback.
        self._reconcile(self._ledger.events())
        return Result("PASS_LOCAL_EFFECT", "READBACK_PASS", final_receipt)
