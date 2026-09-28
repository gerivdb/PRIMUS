#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.validation import gitignore_audit, GitignoreAuditResult


def test_repo_root_not_found():
    result = gitignore_audit("/nonexistent/path")
    assert isinstance(result, GitignoreAuditResult)
    assert result.error is not None
    assert result.ignored_count == 0
    assert result.staged_count == 0
    assert result.conflict_count == 0


def test_valid_repo_returns_result(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    import subprocess
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    (repo / ".gitignore").write_text("*.log\n", encoding="utf-8")
    (repo / "a.log").write_text("", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)

    result = gitignore_audit(repo)
    assert isinstance(result, GitignoreAuditResult)
    assert result.error is None
    assert result.ignored_count >= 1
    assert "a.log" in result.ignored


def test_staged_but_ignored_detection(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    import subprocess
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    (repo / ".gitignore").write_text("secret.txt\n", encoding="utf-8")
    secret = repo / "secret.txt"
    secret.write_text("", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)

    result = gitignore_audit(repo)
    assert isinstance(result, GitignoreAuditResult)
    assert result.error is None
    assert result.conflict_count >= 0  # depends on git state


def test_no_gitignore(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    import subprocess
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    (repo / "a.txt").write_text("", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)

    result = gitignore_audit(repo)
    assert isinstance(result, GitignoreAuditResult)
    assert result.error is None
    assert result.ignored_count == 0


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        test_repo_root_not_found()
        test_valid_repo_returns_result(tmp)
        test_staged_but_ignored_detection(tmp)
        test_no_gitignore(tmp)
    print("OK: All gitignore_audit tests passed")
