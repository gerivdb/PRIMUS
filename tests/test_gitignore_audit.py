"""Tests pour primitives/validation/gitignore_audit.py."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import pytest

from primitives.validation.gitignore_audit import GitignoreAuditResult, gitignore_audit

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_audit_returns_typed_result():
    result = gitignore_audit(REPO_ROOT)
    assert isinstance(result, GitignoreAuditResult)
    assert result.repo_root == str(REPO_ROOT)
    assert isinstance(result.ignored_count, int)
    assert isinstance(result.staged_count, int)
    assert isinstance(result.staged_but_ignored_count, int)
    assert isinstance(result.gitignore_exists, bool)
    assert isinstance(result.gitignore_bytes, int)
    assert result.error is None or isinstance(result.error, str)


def test_audit_temporary_repo():
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "init", tmp], check=True, capture_output=True)
        (Path(tmp) / ".gitignore").write_text("*.pyc\n", encoding="utf-8")
        (Path(tmp) / "foo.pyc").write_text("", encoding="utf-8")
        subprocess.run(["git", "-C", tmp, "add", "."], check=True, capture_output=True)

        result = gitignore_audit(tmp)
        assert result.gitignore_exists is True
        assert result.ignored_count >= 1
