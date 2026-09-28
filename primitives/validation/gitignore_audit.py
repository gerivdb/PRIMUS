#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : gitignore_audit
Catégorie : validation
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Liste les fichiers ignorés par .gitignore dans un repo git.
  Détecte les fichiers staged qui sont aussi ignorés.

Contrat :
  - Input  : repo_root: str | Path
  - Output : GitignoreAuditResult  {ignored, staged, staged_but_ignored, error}
  - Side effects: none (lecture seule)
  - Dépendances: stdlib uniquement
"""
from dataclasses import dataclass, field
from pathlib import Path
import subprocess
import sys


@dataclass
class GitignoreAuditResult:
    ignored: list[str] = field(default_factory=list)
    staged: list[str] = field(default_factory=list)
    staged_but_ignored: list[str] = field(default_factory=list)
    error: str | None = None

    @property
    def ignored_count(self) -> int:
        return len(self.ignored)

    @property
    def staged_count(self) -> int:
        return len(self.staged)

    @property
    def conflict_count(self) -> int:
        return len(self.staged_but_ignored)


def _run_git(repo_root: Path, args: list[str]) -> str | None:
    """Run a git command and return stdout, or None on error."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root)] + args,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def gitignore_audit(repo_root: str | Path) -> GitignoreAuditResult:
    """Audit .gitignore coverage for a git repo."""
    repo_root = Path(repo_root)

    if not repo_root.is_dir():
        return GitignoreAuditResult(error=f"Repository root not found: {repo_root}")

    stdout = _run_git(repo_root, ["ls-files", "--others", "--ignored", "--exclude-standard"])
    ignored = [line for line in (stdout or "").splitlines() if line]

    stdout = _run_git(repo_root, ["diff", "--cached", "--name-only"])
    staged = [line for line in (stdout or "").splitlines() if line]

    staged_set = set(staged)
    staged_but_ignored = [f for f in ignored if f in staged_set]

    return GitignoreAuditResult(
        ignored=ignored,
        staged=staged,
        staged_but_ignored=staged_but_ignored,
    )


if __name__ == "__main__":
    import json

    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    result = gitignore_audit(repo)
    payload = {
        "ignored_count": result.ignored_count,
        "staged_count": result.staged_count,
        "conflict_count": result.conflict_count,
        "ignored": result.ignored[:20],
        "staged_but_ignored": result.staged_but_ignored,
        "error": result.error,
    }
    print(json.dumps(payload, indent=2))
    sys.exit(1 if result.error else 0)
