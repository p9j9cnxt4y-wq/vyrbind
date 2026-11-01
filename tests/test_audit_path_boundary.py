"""Physical audit/workspace separation using real filesystem aliases."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from vyrbind import EvidenceLedger, IntegrityError, Intent, LocalBroker, RunContract


class AuditPathBoundary(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="fpg-audit-boundary-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve(strict=True)
        self.actual = self.base / "actual"
        self.workspace = self.actual / "workspace"
        self.evidence = self.actual / "evidence"
        self.workspace.mkdir(parents=True)
        self.evidence.mkdir()

    def ancestor_alias(self):
        alias = self.base / "alias"
        if os.name == "nt":
            created = subprocess.run(
                [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c",
                 "mklink /J alias actual"],
                cwd=self.base, capture_output=True, timeout=10, check=False,
            )
            self.assertEqual(created.returncode, 0, "Real junction creation failed")
            # Remove only our junction, before TemporaryDirectory cleans its target.
            self.addCleanup(os.rmdir, alias)
        else:
            alias.symlink_to(self.actual, target_is_directory=True)
        self.assertTrue(alias.samefile(self.actual))
        self.assertFalse((alias / "workspace").is_symlink())
        return alias

    def assert_inside_rejected(self, workspace, audit):
        before = sorted(str(p.relative_to(self.actual)) for p in self.actual.rglob("*"))
        contract = RunContract("boundary-scope", "boundary-run", workspace, audit)
        with self.assertRaisesRegex(IntegrityError, "^AUDIT_INSIDE_WORKSPACE$"):
            with LocalBroker(contract):
                self.fail("An audit inside the workspace must never open")
        after = sorted(str(p.relative_to(self.actual)) for p in self.actual.rglob("*"))
        self.assertEqual(after, before, "Rejection must precede DB, lock and journal creation")

    def assert_external_readback(self, workspace, audit):
        contract = RunContract("boundary-scope", "boundary-run", workspace, audit)
        intent = Intent("boundary-run", "boundary-scope", "create-1",
                        "artifact.create_text", "verified.txt", "verified\n")
        with LocalBroker(contract) as broker:
            self.assertEqual(broker.invoke(intent).status, "PASS_LOCAL_EFFECT")
        self.assertEqual((self.workspace / "verified.txt").read_text(), "verified\n")
        ledger = EvidenceLedger(audit, readonly=True)
        try:
            self.assertEqual(ledger.head()[0], 3)
        finally:
            ledger.close()
        self.assertEqual(sorted(p.name for p in audit.parent.iterdir()), ["audit.sqlite"])

    def test_dotdot_inside_is_rejected_before_writes(self):
        audit = self.evidence / ".." / "workspace" / "audit.sqlite"
        self.assert_inside_rejected(self.workspace, audit)

    def test_both_paths_under_alias_inside_are_rejected(self):
        alias = self.ancestor_alias()
        workspace = alias / "workspace"
        self.assert_inside_rejected(workspace, workspace / "audit.sqlite")

    def test_only_audit_under_alias_inside_is_rejected(self):
        alias = self.ancestor_alias()
        self.assert_inside_rejected(self.workspace, alias / "workspace" / "audit.sqlite")

    def test_only_workspace_under_alias_inside_is_rejected(self):
        alias = self.ancestor_alias()
        self.assert_inside_rejected(alias / "workspace", self.workspace / "audit.sqlite")

    def test_nested_audit_under_alias_inside_is_rejected(self):
        (self.workspace / "nested").mkdir()
        alias = self.ancestor_alias()
        self.assert_inside_rejected(self.workspace, alias / "workspace" / "nested" / "audit.sqlite")

    def test_alias_sibling_audit_allows_verified_effect(self):
        alias = self.ancestor_alias()
        self.assert_external_readback(alias / "workspace", alias / "evidence" / "audit.sqlite")

    def test_prefix_sibling_is_outside_workspace(self):
        sibling = self.actual / "workspace-evidence"
        sibling.mkdir()
        self.assert_external_readback(self.workspace, sibling / "audit.sqlite")

    def test_case_alias_inside_is_rejected_on_case_insensitive_filesystem(self):
        variant = self.actual / "WORKSPACE"
        if not variant.exists() or not variant.samefile(self.workspace):
            self.skipTest("Fixture filesystem does not provide this case alias")
        (self.workspace / "nested").mkdir()
        self.assert_inside_rejected(self.workspace, variant / "nested" / "audit.sqlite")

    def test_distinct_case_sibling_is_allowed_on_case_sensitive_filesystem(self):
        variant = self.actual / "WORKSPACE"
        if variant.exists():
            self.skipTest("Fixture filesystem does not provide distinct case siblings")
        variant.mkdir()
        self.assertFalse(variant.samefile(self.workspace))
        self.assert_external_readback(self.workspace, variant / "audit.sqlite")

    def test_alias_does_not_bypass_untracked_node_guard(self):
        alias = self.ancestor_alias()
        (self.workspace / "untracked.py").write_text("inert synthetic content")
        contract = RunContract("boundary-scope", "boundary-run", alias / "workspace",
                               alias / "evidence" / "audit.sqlite")
        with self.assertRaisesRegex(IntegrityError, "^UNTRACKED_NODE_IN_WORKSPACE$"):
            with LocalBroker(contract):
                self.fail("Untracked node accepted")
        self.assertEqual(sorted(p.name for p in self.workspace.iterdir()), ["untracked.py"])

    def test_alias_does_not_bypass_untracked_artifact_guard(self):
        alias = self.ancestor_alias()
        (self.workspace / "unknown.txt").write_text("inert synthetic content")
        contract = RunContract("boundary-scope", "boundary-run", alias / "workspace",
                               alias / "evidence" / "audit.sqlite")
        with self.assertRaisesRegex(IntegrityError, "^UNTRACKED_ARTIFACT$"):
            with LocalBroker(contract):
                self.fail("Untracked artifact accepted")
        self.assertEqual(sorted(p.name for p in self.workspace.iterdir()), ["unknown.txt"])

    def make_symlink(self, link, target, *, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError):
            self.skipTest("Real symlink creation unavailable")

    def test_direct_audit_parent_symlink_is_still_rejected(self):
        link = self.base / "evidence-link"
        self.make_symlink(link, self.evidence, directory=True)
        contract = RunContract("boundary-scope", "boundary-run", self.workspace, link / "audit.sqlite")
        with self.assertRaisesRegex(IntegrityError, "^UNTRUSTED_AUDIT_PARENT$"):
            with LocalBroker(contract):
                self.fail("Direct audit parent symlink accepted")
        self.assertEqual(list(self.evidence.iterdir()), [])

    def test_audit_leaf_symlink_is_still_rejected(self):
        target = self.base / "existing-target"
        target.write_bytes(b"unchanged synthetic bytes")
        audit = self.evidence / "audit.sqlite"
        self.make_symlink(audit, target)
        contract = RunContract("boundary-scope", "boundary-run", self.workspace, audit)
        with self.assertRaisesRegex(IntegrityError, "^INVALID_AUDIT_FILE$"):
            with LocalBroker(contract):
                self.fail("Audit leaf symlink accepted")
        self.assertEqual(target.read_bytes(), b"unchanged synthetic bytes")
        self.assertEqual(sorted(p.name for p in self.evidence.iterdir()), ["audit.sqlite"])


if __name__ == "__main__":
    unittest.main()
