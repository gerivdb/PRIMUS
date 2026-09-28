"""Tests pour primitives/validation/mcp_scope_check.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from primitives.validation.mcp_scope_check import McpScopeResult, mcp_scope_check


def test_mcp_scope_devtools():
    result = mcp_scope_check(r"C:\DevTools")
    assert isinstance(result, McpScopeResult)
    assert result.mcp_scope is True
    assert result.recommended_tool == "mcp"


def test_shell_scope_temp_kilo():
    result = mcp_scope_check(r"C:\Users\GG\AppData\Local\Temp\kilo")
    assert isinstance(result, McpScopeResult)
    assert result.shell_scope is True
    assert result.recommended_tool == "shell"


def test_blocked_path():
    result = mcp_scope_check("X:\\outside\\scope")
    assert isinstance(result, McpScopeResult)
    assert result.recommended_tool == "blocked"
