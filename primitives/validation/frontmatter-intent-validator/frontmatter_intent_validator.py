#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : frontmatter_intent_validator
Catégorie : validation
Spec      : ONTOLOGY/primitives/ (voir schema ci-dessous)

Responsabilité unique :
  Valide le frontmatter YAML d'un fichier INTENT.
  Vérifie: intent_hash format, status, priority, presence of required sections.

Contrat :
  - Input  : file_path: str (path to INTENT-*.md)
  - Output : ValidationResult  {valid, errors, error_count}
  - Side effects: none
  - Dependances: stdlib uniquement
"""
import re
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ValidationError:
    path: str
    message: str
    value: object = None


@dataclass
class ValidationResult:
    valid: bool
    errors: list[ValidationError] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return len(self.errors)

    def first_error(self) -> ValidationError | None:
        return self.errors[0] if self.errors else None

    def __bool__(self) -> bool:
        return self.valid


REQUIRED_SECTIONS = [
    "## 1. RESUME EXECUTIF",
    "## 2. METAPHORE FONDATRICE",
    "## 3. KG-L",
    "## 4. ARCHITECTURE PAR STRATES",
    "## 5. CONTRATS DE RESPONSABILITE",
    "## 6. PHI-CPS CONCRET",
    "## 10. METRIQUES DE SUCCES",
    "## 27. CONCLUSION FINALE",
]

VALID_STATUSES = {"proposed", "accepted", "deprecated", "superseded", "archived"}
VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}


def _read_frontmatter_and_sections(file_path: str | Path) -> tuple[dict[str, str], str]:
    text = Path(file_path).read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    fm = text[3:end].strip()
    body = text[end + 3 :]
    meta: dict[str, str] = {}
    for line in fm.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta, text


def frontmatter_intent_validator(file_path: str | Path) -> ValidationResult:
    errors: list[ValidationError] = []
    path = Path(file_path)

    if not path.exists():
        return ValidationResult(valid=False, errors=[ValidationError(path=str(path), message="File not found")])

    meta, full_text = _read_frontmatter_and_sections(file_path)

    # intent_hash format
    intent_hash = meta.get("intent_hash", "")
    if not re.fullmatch(r"0x[A-Za-z0-9_-]+", intent_hash):
        errors.append(ValidationError(path=str(path), message="intent_hash must match 0x[A-Za-z0-9_-]+", value=intent_hash))

    # status
    status = meta.get("status", "")
    if status not in VALID_STATUSES:
        errors.append(ValidationError(path=str(path), message=f"status must be one of {VALID_STATUSES}", value=status))

    # priority
    priority = meta.get("priority", "")
    if priority not in VALID_PRIORITIES:
        errors.append(ValidationError(path=str(path), message=f"priority must be one of {VALID_PRIORITIES}", value=priority))

    # required sections
    for section in REQUIRED_SECTIONS:
        if section not in full_text:
            errors.append(ValidationError(path=str(path), message=f"Missing required section: {section}"))

    return ValidationResult(valid=len(errors) == 0, errors=errors)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python frontmatter_intent_validator.py <intent_file.md>")
        raise SystemExit(1)
    result = frontmatter_intent_validator(sys.argv[1])
    if result.valid:
        print("VALID")
    else:
        for err in result.errors:
            print(f"INVALID: {err.path}: {err.message} (value={err.value})")
        raise SystemExit(2)
