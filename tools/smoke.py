"""Real local clean-room create -> readback -> verify -> denial, no network."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

project = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project / "src"))

from forgeproofgate import EvidenceLedger, Intent, LocalBroker, RunContract

with tempfile.TemporaryDirectory(prefix="fpg-local-smoke-") as tmp:
    root = Path(tmp)
    workspace, evidence = root / "output", root / "evidence"
    workspace.mkdir()
    evidence.mkdir()
    contract = RunContract("smoke-scope", "smoke-run", workspace, evidence / "events.sqlite")
    action = Intent.from_mapping({
        "scope_id": "smoke-scope", "run_id": "smoke-run", "action_id": "create-001",
        "operation": "artifact.create_text", "target": "checked.txt",
        "content": "local-check\n",
    })
    with LocalBroker(contract) as broker:
        allowed = broker.invoke(action)
        denied = broker.invoke(Intent.from_mapping({
            "scope_id": "smoke-scope", "run_id": "smoke-run", "action_id": "deploy-002",
            "operation": "deploy.apply", "target": "out.txt", "content": "no deploy",
        }))
    ledger = EvidenceLedger(contract.audit_db, readonly=True)
    try:
        count, head = ledger.head()
    finally:
        ledger.close()
    assert allowed.status == "PASS_LOCAL_EFFECT", allowed
    assert denied.status == "HUMAN_GATE_REQUIRED", denied
    assert (workspace / "checked.txt").read_text() == "local-check\n"
    assert not (workspace / "out.txt").exists()
    assert count == 4
    print(json.dumps({"status": "PASS", "real_local_write": True,
                      "unapproved_deploy_effect": False, "audit_events": count,
                      "audit_head_sha256": head}, sort_keys=True))
