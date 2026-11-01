"""Small SQLite SHA-256-linked evidence ledger.

A hash chain detects accidental edits and straightforward tampering. It is NOT
cryptographic authenticity against an attacker who can rewrite the whole DB.
A separately stored, independently trusted head-hash anchor is necessary.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import time

_GENESIS = "0" * 64
_PHASES = frozenset({"CONTRACT_BIND", "DECISION_ALLOW", "DECISION_DENY", "EFFECT_OK", "EFFECT_UNKNOWN"})
_MAX_EVENTS = 10_000


class IntegrityError(RuntimeError):
    """Fail closed: a claimed evidence record could not be independently checked."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(value: str) -> str:
    return sha256(value.encode("utf-8"))


def _canonical(mapping: dict) -> bytes:
    return json.dumps(mapping, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass(frozen=True, slots=True)
class Event:
    seq: int
    timestamp_ns: int
    phase: str
    action_hash: str
    target_hash: str
    content_hash: str
    code: str
    prev_hash: str
    event_hash: str

    def digest_payload(self) -> dict:
        return {"seq": self.seq, "timestamp_ns": self.timestamp_ns, "phase": self.phase,
                "action_hash": self.action_hash, "target_hash": self.target_hash,
                "content_hash": self.content_hash, "code": self.code,
                "prev_hash": self.prev_hash}


def _check_audit_path(path: Path) -> None:
    if not path.is_absolute() or not path.parent.is_dir() or path.parent.is_symlink():
        raise IntegrityError("INVALID_AUDIT_LOCATION")
    try:
        node = path.lstat()
    except FileNotFoundError:
        return
    if not stat.S_ISREG(node.st_mode):
        raise IntegrityError("INVALID_AUDIT_FILE")


class EvidenceLedger:
    def __init__(self, path: Path, *, readonly: bool = False) -> None:
        _check_audit_path(path)
        self.path = path
        if readonly and not path.is_file():
            raise IntegrityError("NO_AUDIT_FILE")
        if not readonly and not path.exists():
            # Restrictive creation; operator must protect the parent directory.
            flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
            if hasattr(os, "O_BINARY"):
                flags |= os.O_BINARY
            try:
                fd = os.open(path, flags, 0o600)
            except FileExistsError:
                raise IntegrityError("AUDIT_RACE") from None
            else:
                os.close(fd)
        try:
            if readonly:
                self.conn = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=2, isolation_level=None)
            else:
                self.conn = sqlite3.connect(str(path), timeout=2, isolation_level=None)
            self.conn.execute("PRAGMA busy_timeout=2000")
            if not readonly:
                self.conn.execute("PRAGMA journal_mode=DELETE")
                self.conn.execute("PRAGMA synchronous=FULL")
                self.conn.execute("""CREATE TABLE IF NOT EXISTS events (
                    seq INTEGER PRIMARY KEY,
                    timestamp_ns INTEGER NOT NULL,
                    phase TEXT NOT NULL,
                    action_hash TEXT NOT NULL,
                    target_hash TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    code TEXT NOT NULL,
                    prev_hash TEXT NOT NULL,
                    event_hash TEXT NOT NULL
                )""")
        except sqlite3.DatabaseError as exc:
            if hasattr(self, "conn"):
                self.conn.close()
            raise IntegrityError("AUDIT_OPEN_FAILED") from exc
        self._readonly = readonly

    def close(self) -> None:
        self.conn.close()

    def events(self) -> list[Event]:
        try:
            rows = self.conn.execute("SELECT seq,timestamp_ns,phase,action_hash,target_hash,content_hash,code,prev_hash,event_hash FROM events ORDER BY seq").fetchall()
        except sqlite3.DatabaseError as exc:
            raise IntegrityError("AUDIT_READ_FAILED") from exc
        if len(rows) > _MAX_EVENTS:
            raise IntegrityError("AUDIT_LIMIT_REACHED")
        records = [Event(*row) for row in rows]
        prior = _GENESIS
        for expected_seq, entry in enumerate(records, start=1):
            if (entry.seq != expected_seq or entry.phase not in _PHASES
                    or entry.prev_hash != prior or not isinstance(entry.code, str)):
                raise IntegrityError("AUDIT_CHAIN_INVALID")
            if (not all(isinstance(x, str) and len(x) == 64 and
                        all(c in "0123456789abcdef" for c in x)
                        for x in (entry.action_hash, entry.target_hash, entry.content_hash, entry.prev_hash, entry.event_hash))):
                raise IntegrityError("AUDIT_FIELDS_INVALID")
            if sha256(_canonical(entry.digest_payload())) != entry.event_hash:
                raise IntegrityError("AUDIT_HASH_MISMATCH")
            prior = entry.event_hash
        return records

    def head(self) -> tuple[int, str]:
        rows = self.events()
        return len(rows), rows[-1].event_hash if rows else _GENESIS

    def append(self, *, phase: str, action_hash: str, target_hash: str, content_hash: str,
               code: str) -> str:
        if self._readonly:
            raise IntegrityError("AUDIT_READ_ONLY")
        if phase not in _PHASES or not code.isascii() or not code.replace("_", "").isalnum() or len(code) > 60:
            raise IntegrityError("INVALID_AUDIT_EVENT")
        try:
            self.conn.execute("BEGIN IMMEDIATE")
            previous = self.events()  # verify under transaction before every append
            if len(previous) >= _MAX_EVENTS:
                raise IntegrityError("AUDIT_LIMIT_REACHED")
            entry = Event(
                seq=len(previous) + 1, timestamp_ns=time.time_ns(), phase=phase,
                action_hash=action_hash, target_hash=target_hash,
                content_hash=content_hash, code=code,
                prev_hash=previous[-1].event_hash if previous else _GENESIS,
                event_hash="",
            )
            computed = sha256(_canonical(entry.digest_payload()))
            self.conn.execute(
                "INSERT INTO events(seq,timestamp_ns,phase,action_hash,target_hash,content_hash,code,prev_hash,event_hash) VALUES(?,?,?,?,?,?,?,?,?)",
                (entry.seq, entry.timestamp_ns, entry.phase, entry.action_hash,
                 entry.target_hash, entry.content_hash, entry.code, entry.prev_hash, computed),
            )
            self.conn.execute("COMMIT")
            return computed
        except Exception as exc:
            try:
                self.conn.execute("ROLLBACK")
            except sqlite3.DatabaseError:
                pass
            if isinstance(exc, IntegrityError):
                raise
            raise IntegrityError("AUDIT_APPEND_FAILED") from exc
