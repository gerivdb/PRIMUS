#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.validation.yaml_editor import yaml_editor, YamlWriteResult


def test_write_yaml(tmp_path: Path):
    target = tmp_path / "out.yaml"
    result = yaml_editor(target, {"key": "value"})
    assert isinstance(result, YamlWriteResult)
    assert result.error is None
    assert result.bytes_written > 0
    assert target.exists()


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        test_write_yaml(tmp)
    print("OK: All yaml_editor tests passed")
