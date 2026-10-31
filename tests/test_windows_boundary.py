"""Real Windows junction coverage for the workspace reparse-point boundary."""
from __future__ import annotations

import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from forgeproofgate import IntegrityError, LocalBroker, RunContract


@unittest.skipUnless(os.name == "nt", "Windows junction fixture requires Windows")
class WindowsWorkspaceBoundary(unittest.TestCase):
    def test_real_junction_is_refused_without_junction_helper(self):
        with tempfile.TemporaryDirectory(prefix="fpg-junction-") as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            evidence = root / "evidence"
            junction = root / "junction"
            workspace.mkdir()
            evidence.mkdir()
            audit = evidence / "audit.sqlite"
            contract = RunContract("junction-scope", "junction-run", junction, audit)
            # Fixed relative names keep filesystem paths out of shell syntax.
            # The junction is real; no filesystem result is mocked.
            created = subprocess.run(
                [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c",
                 "mklink /J junction workspace"],
                cwd=root, capture_output=True, timeout=10, check=False,
            )
            try:
                self.assertEqual(created.returncode, 0, "Windows junction creation failed")
                node = junction.lstat()
                self.assertTrue(node.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
                self.assertEqual(node.st_reparse_tag, stat.IO_REPARSE_TAG_MOUNT_POINT)
                self.assertEqual(junction.resolve(strict=True), workspace.resolve(strict=True))
                # Exercise the attribute guard independently of the convenience
                # helper, which is unavailable in Python 3.11. This does not
                # substitute for running CI on that Python version.
                with patch.object(type(junction), "is_junction", return_value=False, create=True):
                    with self.assertRaisesRegex(IntegrityError, "^UNTRUSTED_WORKSPACE$"):
                        with LocalBroker(contract):
                            self.fail("A junction workspace must never open")
                self.assertEqual(list(workspace.iterdir()), [])
                self.assertEqual(list(evidence.iterdir()), [])
            finally:
                if os.path.lexists(junction):
                    # Remove only this test's junction, never traverse its target.
                    os.rmdir(junction)


if __name__ == "__main__":
    unittest.main()
