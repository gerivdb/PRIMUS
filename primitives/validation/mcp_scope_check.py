#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : mcp_scope_check
Catégorie : validation
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Détermine si un chemin est accessible via MCP filesystem,
  shell, ou bloqué.

Contrat :
  - Input  : path: str | Path
  - Output : McpScopeResult
  - Side effects: none
  - Dépendances: stdlib only
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class McpScopeResult:
    path: str = ""
    exists: bool = False
    mcp_scope: bool = False
    shell_scope: bool = False
    recommended_tool: str = ""
    error: str | None = None


ALLOWED_MCP_DIRS = [
    r"C:\DevTools",
    r"D:\DO\WEB",
]

SHELL_ALWAYS_OK = [
    r"C:\DevTools",
    r"D:\DO\WEB",
    r"C:\Users\GG\AppData\Local\Temp\kilo",
]


def _under_any(path: Path, bases: list[str]) -> bool:
    for base in bases:
        try:
            path.relative_to(Path(base).resolve())
            return True
        except ValueError:
            continue
    return False


def mcp_scope_check(path: str | Path) -> McpScopeResult:
    p = Path(path).resolve()
    exists = p.exists()
    mcp_scope = _under_any(p, ALLOWED_MCP_DIRS)
    shell_scope = _under_any(p, SHELL_ALWAYS_OK)
    if mcp_scope:
        recommended_tool = "mcp"
    elif shell_scope:
        recommended_tool = "shell"
    else:
        recommended_tool = "blocked"
    return McpScopeResult(
        path=str(p),
        exists=exists,
        mcp_scope=mcp_scope,
        shell_scope=shell_scope,
        recommended_tool=recommended_tool,
    )


if __name__ == "__main__":
    import json

    target = sys.argv[1] if len(sys.argv) > 1 else str(Path.cwd())
    result = mcp_scope_check(target)
    payload = {
        "path": result.path,
        "exists": result.exists,
        "mcp_scope": result.mcp_scope,
        "shell_scope": result.shell_scope,
        "recommended_tool": result.recommended_tool,
        "error": result.error,
    }
    print(json.dumps(payload, indent=2))
    sys.exit(2 if result.recommended_tool == "blocked" else 0)
