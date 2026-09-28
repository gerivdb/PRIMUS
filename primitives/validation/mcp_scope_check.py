#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : mcp_scope_check
Catégorie : validation
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Détermine si un chemin est accessible via MCP filesystem
  ou nécessite bash/PowerShell.

Contrat :
  - Input  : path: str
  - Output : McpScopeResult  {path, exists, mcp_scope, shell_scope, recommended_tool}
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class McpScopeResult:
    path: str
    exists: bool
    mcp_scope: bool
    shell_scope: bool
    recommended_tool: str


ALLOWED_MCP_DIRS = [
    r"C:\DevTools",
    r"D:\DO\WEB",
]

SHELL_ALWAYS_OK = [
    r"C:\DevTools",
    r"D:\DO\WEB",
    r"C:\Users\GG\AppData\Local\Temp\kilo",
]


def _under_any(path: str, dirs: list[str]) -> bool:
    p = Path(path).resolve()
    for allowed in dirs:
        try:
            p.relative_to(Path(allowed).resolve())
            return True
        except ValueError:
            continue
    return False


def mcp_scope_check(path: str) -> McpScopeResult:
    """Check if a path is accessible via MCP filesystem or shell."""
    p = Path(path).resolve()
    exists = p.exists()
    mcp_scope = _under_any(path, ALLOWED_MCP_DIRS)
    shell_scope = _under_any(path, SHELL_ALWAYS_OK)

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
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = mcp_scope_check(path)
    print(json.dumps({
        "path": result.path,
        "exists": result.exists,
        "mcp_scope": result.mcp_scope,
        "shell_scope": result.shell_scope,
        "recommended_tool": result.recommended_tool,
    }, indent=2))
    sys.exit(2 if result.recommended_tool == "blocked" else 0)
