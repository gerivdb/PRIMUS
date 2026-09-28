#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : yaml_editor
Catégorie : validation
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Écrit un dictionnaire Python dans un fichier YAML.

Contrat :
  - Input  : path: str | Path, data: dict
  - Output : YamlWriteResult  {path, bytes_written, error}
  - Side effects: écriture fichier
  - Dépendances: stdlib + yaml (PyYAML)
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass
class YamlWriteResult:
    path: str = ""
    bytes_written: int = 0
    error: str | None = None


def yaml_editor(path: str | Path, data: dict) -> YamlWriteResult:
    try:
        import yaml
    except ImportError as exc:
        return YamlWriteResult(error=f"PyYAML required: {exc}")

    target = Path(path)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
        target.write_text(text, encoding="utf-8")
        return YamlWriteResult(path=str(target), bytes_written=len(text.encode("utf-8")))
    except Exception as exc:
        return YamlWriteResult(error=str(exc))


if __name__ == "__main__":
    import json
    import sys

    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    result = yaml_editor(data.get("path", ""), data.get("data", {}))
    print(json.dumps({
        "path": result.path,
        "bytes_written": result.bytes_written,
        "error": result.error,
    }, indent=2))
    sys.exit(1 if result.error else 0)
