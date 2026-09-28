"""Tests pour primitives/logic/generate_validation_report.py."""

from __future__ import annotations

import pytest

from primitives.logic.generate_validation_report import (
    ValidationReportResult,
    generate_validation_report,
)


def test_all_pass():
    results = [
        {"name": "test_a", "status": "PASS", "exit_code": 0, "stdout": "", "stderr": ""},
        {"name": "test_b", "status": "PASS", "exit_code": 0, "stdout": "", "stderr": ""},
    ]
    report = generate_validation_report(results)
    assert isinstance(report, ValidationReportResult)
    assert report.summary["total"] == 2
    assert report.summary["passed"] == 2
    assert report.summary["failed"] == 0
    assert report.summary["result"] == "PASS"
    assert len(report.details) == 2


def test_mixed_results():
    results = [
        {"name": "test_a", "status": "PASS", "exit_code": 0, "stdout": "", "stderr": ""},
        {"name": "test_b", "status": "FAIL", "exit_code": 1, "stdout": "", "stderr": "boom"},
    ]
    report = generate_validation_report(results)
    assert report.summary["total"] == 2
    assert report.summary["passed"] == 1
    assert report.summary["failed"] == 1
    assert report.summary["result"] == "FAIL"
    assert report.details[1]["stderr"] == "boom"


def test_empty_results():
    report = generate_validation_report([])
    assert report.summary["total"] == 0
    assert report.summary["result"] == "PASS"
    assert report.details == []
