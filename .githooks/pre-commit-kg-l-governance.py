#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
pre-commit-kg-l-governance.py - Gate de gouvernance KG-L injecte cross-repo (GEN-025 / ADR-2026-08-27-001).

Source de vérité unique : REPO-STANDARDS/.githooks/pre-commit-kg-l-governance.py.
Consommé par tous les repos gerivdb/* (EX-01).

Corrige le défaut hermétique d'origine (ADR-2026-08-27-001 §D1) :
  - GF-15 (validate_designs) ET GF-16 (check_staged_edge_kinds) s'exécutent
    séquentiellement, sans code mort (`return 0` n'interrompt plus GF-16).
  - GF-16 inspecctionne le working tree du CONSOMMATEUR (`--repo-root`), pas
    celui de KG-L.

Portée :
  - repos consommateurs (défaut)        -> GF-16 uniquement (arêtes *.jsonl stagées)
  - KG-L lui-même (env KG_L_GOVERNANCE_SCOPE=kg-l) -> GF-15 + GF-16

Configuration (env, override-safe pour tests/Boot-5ter) :
  KG_L_ROOT               -> D:\DO\WEB\TOOLS\L4-TOOLS\KG-L (canonical)
  KG_L_GOVERNANCE_SCOPE   -> "kg-l" pour activer GF-15
  KG_L_HOOK_TIMEOUT       -> 120s (défaut)

Exit codes : 0 = OK, 1 = BLOCKED (GF-15 ou GF-16).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

DEFAULT_KG_L_ROOT = r"D:\DO\WEB\TOOLS\L4-TOOLS\KG-L"
TIMEOUT = int(os.environ.get("KG_L_HOOK_TIMEOUT", "120"))


def repo_root() -> str:
    """Chemin absolu du repo consommateur (celui où le hook est installé)."""
    r = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, errors="ignore",
    )
    return (r.stdout.strip() or os.getcwd()).replace("/", "\\")


def kg_root() -> str:
    return os.environ.get("KG_L_ROOT", DEFAULT_KG_L_ROOT).replace("/", "\\")


def run(script: str, args: list[str]) -> tuple[int, str, str]:
    cmd = [sys.executable, script, *args]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       errors="ignore", timeout=TIMEOUT)
    return r.returncode, r.stdout, r.stderr


def main() -> int:
    root = repo_root()
    kgl = kg_root()
    scope = os.environ.get("KG_L_GOVERNANCE_SCOPE", "")
    log: list[str] = []

    # --- GF-16 : gate des kinds d'arêtes sur les *.jsonl stagés du consommateur ---
    gf16 = Path(kgl) / "scripts" / "check_staged_edge_kinds.py"
    if not gf16.exists():
        print(f"[KG-L-GATE] SKIP GF-16: {gf16} not found")
    else:
        log.append("[KG-L-GATE] GF-16 : validation des kinds d'arêtes stagées")
        rc, out, err = run(str(gf16), ["--repo-root", root])
        if out.strip():
            print(out.rstrip())
        if err.strip():
            print(err.rstrip(), file=sys.stderr)
        if rc != 0:
            print("\n[KG-L-GATE] BLOCKED : GF-16 (edge-kind) refusé.")
            return 1

    # --- GF-15 : ne s'applique qu'au repo KG-L lui-même (scope=kg-l) ---
    if scope == "kg-l":
        gf15 = Path(kgl) / "scripts" / "validate_designs.py"
        if not gf15.exists():
            print(f"[KG-L-GATE] SKIP GF-15: {gf15} not found")
        else:
            log.append("[KG-L-GATE] GF-15 : validation des designs unified-design")
            rc, out, err = run(str(gf15), ["--scope", "kg-l"])
            if out.strip():
                print(out.rstrip())
            if err.strip():
                print(err.rstrip(), file=sys.stderr)
            if rc != 0:
                print("\n[KG-L-GATE] BLOCKED : GF-15 (designs) refusé.")
                return 1

    print("[KG-L-GATE] OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
