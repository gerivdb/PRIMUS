#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : gitignore_audit
Catégorie : validation
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Audit .gitignore d'un dépôt git : fichiers ignorés, fichiers staged,
  fichiers staged mais ignorés.

Contrat :
  - Input  : repo_root: str | Path
  - Output : GitignoreAuditResult
  - Side effects: lecture git, pas de modification
  - Dépendances: stdlib only
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GitignoreAuditResult:
    repo_root: str = ""
    ignored_count: int = 0
    staged_count: int = 0
    staged_but_ignored_count: int = 0
    staged_but_ignored: list[str] | None = None
    gitignore_exists: bool = False
    gitignore_bytes: int = 0
    error: str | None = None


def _get_ignored_files(repo_root: str) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", repo_root, "ls-files", "--others", "--ignored", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [line for line in result.stdout.strip().split("\n") if line]
    except subprocess.CalledProcessError as exc:
        return [f"ERROR: {exc.stderr}"]


def _get_staged_files(repo_root: str) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", repo_root, "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [line for line in result.stdout.strip().split("\n") if line]
    except subprocess.CalledProcessError:
        return []


def gitignore_audit(repo_root: str | Path) -> GitignoreAuditResult:
    root = str(repo_root)
    ignored = _get_ignored_files(root)
    staged = _get_staged_files(root)
    staged_but_ignored = [f for f in staged if f in ignored]
    gitignore_path = Path(root) / ".gitignore"
    return GitignoreAuditResult(
        repo_root=root,
        ignored_count=len(ignored),
        staged_count=len(staged),
        staged_but_ignored_count=len(staged_but_ignored),
        staged_but_ignored=staged_but_ignored,
        gitignore_exists=gitignore_path.exists(),
        gitignore_bytes=gitignore_path.stat().st_size if gitignore_path.exists() else 0,
    )


if __name__ == "__main__":
    import json

    repo_root = sys.argv[1] if len(sys.argv) > 1 else str(Path.cwd())
    result = gitignore_audit(repo_root)
    payload = {
        "repo_root": result.repo_root,
        "ignored_count": result.ignored_count,
        "staged_count": result.staged_count,
        "staged_but_ignored_count": result.staged_but_ignored_count,
        "staged_but_ignored": result.staged_but_ignored,
        "gitignore_exists": result.gitignore_exists,
        "gitignore_bytes": result.gitignore_bytes,
        "error": result.error,
    }
    print(json.dumps(payload, indent=2))
    sys.exit(1 if result.error else 0)
