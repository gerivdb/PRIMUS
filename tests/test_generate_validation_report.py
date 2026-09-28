#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.logic.reporting.generate_validation_report import generate_validation_report, ValidationReport


def test_report_mixed_results():
    results = [
        {"name": "a", "passed": True},
        {"name": "b", "passed": False},
        {"name": "c", "passed": True},
    ]
    report = generate_validation_report(results)
    assert isinstance(report, ValidationReport)
    assert report.total == 3
    assert report.passed == 2
    assert report.failed == 1
    assert report.summary["pass_rate"] == 2 / 3


def test_report_all_passed():
    results = [{"name": "a", "passed": True}]
    report = generate_validation_report(results)
    assert report.passed == 1
    assert report.failed == 0


def test_report_empty():
    report = generate_validation_report([])
    assert report.total == 0
    assert report.summary["pass_rate"] == 0.0


if __name__ == "__main__":
    test_report_mixed_results()
    test_report_all_passed()
    test_report_empty()
    print("OK: All generate_validation_report tests passed")
