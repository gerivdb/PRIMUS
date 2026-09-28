#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.logic.service.service_lifecycle import service_lifecycle, ServiceLifecycleResult


def test_valid_lifecycle():
    services = [
        {"name": "a", "startup_order": 1, "shutdown_order": 2},
    ]
    result = service_lifecycle(services)
    assert isinstance(result, ServiceLifecycleResult)
    assert result.valid is True
    assert result.error_count == 0


def test_missing_order():
    services = [{"name": "a", "startup_order": 1}]
    result = service_lifecycle(services)
    assert result.valid is False
    assert result.error_count == 1


if __name__ == "__main__":
    test_valid_lifecycle()
    test_missing_order()
    print("OK: All service_lifecycle tests passed")
