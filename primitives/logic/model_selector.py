#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : model_selector
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Sélectionne le meilleur modèle candidat selon une taille minimale.

Contrat :
  - Input  : models: list[dict], min_size_mb: int
  - Output : ModelSelectorResult
  - Side effects: none
  - Dépendances: stdlib only
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModelSelectorResult:
    best_model: str | None = None
    best_size_mb: float = 0.0
    all_candidates: list[dict[str, Any]] = field(default_factory=list)


def model_selector(
    models: list[dict[str, Any]],
    min_size_mb: int = 0,
) -> ModelSelectorResult:
    """Retourne le plus petit modèle dont la taille >= min_size_mb."""
    candidates = []
    for model in models:
        name = model.get("name") or model.get("id") or ""
        size_bytes = model.get("size", 0)
        try:
            size_mb = float(size_bytes) / (1024 * 1024)
        except (TypeError, ValueError):
            size_mb = 0.0
        if size_mb >= min_size_mb:
            candidates.append({"name": name, "size_mb": round(size_mb, 2)})

    if not candidates:
        return ModelSelectorResult()

    best = min(candidates, key=lambda item: item["size_mb"])
    return ModelSelectorResult(
        best_model=best["name"],
        best_size_mb=best["size_mb"],
        all_candidates=candidates,
    )


if __name__ == "__main__":
    import json
    import sys

    raw = sys.stdin.read() if sys.stdin.isatty() is False else "{}"
    payload = json.loads(raw)
    models = payload.get("models", [])
    min_size_mb = int(payload.get("min_size_mb", 0))
    result = model_selector(models, min_size_mb=min_size_mb)
    print(json.dumps({
        "best_model": result.best_model,
        "best_size_mb": result.best_size_mb,
        "all_candidates": result.all_candidates,
    }, indent=2))
