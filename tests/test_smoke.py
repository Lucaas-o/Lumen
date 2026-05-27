# tests\test_smoke.py
"""Placeholder tests for Phase 0.

These exist so `pytest` exits cleanly while the project is bootstrapped.
Real tests arrive with each feature in Phase 1+.
"""

from lumen import __version__


def test_version_is_set() -> None:
    assert __version__ == "0.1.0"


def test_cli_module_importable() -> None:
    from lumen.cli.main import app

    assert app is not None
