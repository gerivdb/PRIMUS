"""Tests pour primitives/logic/service_lifecycle.py."""

from __future__ import annotations

import pytest

from primitives.logic.service_lifecycle import ServiceLifecycleResult, service_lifecycle


def test_valid_service_list():
    services = [
        {"name": "jevx", "port": 8082, "startup_order": 6},
        {"name": "ollama", "port": 11434, "startup_order": 4},
    ]
    result = service_lifecycle(services)
    assert isinstance(result, ServiceLifecycleResult)
    assert result.valid is True
    assert result.error_count == 0
    assert result.errors == []


def test_missing_name_and_port():
    services = [
        {"startup_order": 1},
        {"name": "bad", "startup_order": 2},
    ]
    result = service_lifecycle(services)
    assert result.valid is False
    assert result.error_count == 2
    assert any("missing name/id" in err for err in result.errors)
    assert any("missing port" in err for err in result.errors)
