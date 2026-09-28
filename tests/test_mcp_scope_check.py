#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.validation import mcp_scope_check, McpScopeResult


def test_allowed_mcp_path():
    result = mcp_scope_check(r"D:\DO\WEB\TOOLS\L4-TOOLS\PRIMUS")
    assert isinstance(result, McpScopeResult)
    assert result.mcp_scope is True
    assert result.recommended_tool == "mcp"


def test_shell_only_path():
    result = mcp_scope_check(r"C:\Users\GG\AppData\Local\Temp\kilo")
    assert isinstance(result, McpScopeResult)
    assert result.mcp_scope is False
    assert result.shell_scope is True
    assert result.recommended_tool == "shell"


def test_outside_scope():
    result = mcp_scope_check(r"C:\Windows\System32")
    assert isinstance(result, McpScopeResult)
    assert result.recommended_tool == "blocked"


def test_nonexistent_path():
    result = mcp_scope_check(r"C:\nonexistent\path")
    assert isinstance(result, McpScopeResult)
    assert result.exists is False


if __name__ == "__main__":
    test_allowed_mcp_path()
    test_shell_only_path()
    test_outside_scope()
    test_nonexistent_path()
    print("OK: All mcp_scope_check tests passed")
