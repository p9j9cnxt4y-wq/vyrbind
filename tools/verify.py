"""Dependency-free source test runner for new checkouts."""
from pathlib import Path
import sys
import unittest

project = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project / "src"))

suite = unittest.defaultTestLoader.discover(str(project / "tests"), pattern="test_*.py")
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
