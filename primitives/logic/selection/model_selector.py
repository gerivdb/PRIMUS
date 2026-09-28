#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : model_selector
Catégorie : logic/selection
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Sélectionne le meilleur modèle d'une liste selon un critère de taille.

Contrat :
  - Input  : models: list[dict], min_size_mb: int = 0
  - Output : ModelSelectionResult  {best_model, best_size_mb, all_candidates}
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
from dataclasses import dataclass, field


@dataclass
class ModelSelectionResult:
    best_model: str | None = None
    best_size_mb: float = 0.0
    all_candidates: list[dict] = field(default_factory=list)


def model_selector(models: list[dict], min_size_mb: int = 0) -> ModelSelectionResult:
    candidates = []
    for model in models:
        name = model.get("name", "")
        size_bytes = model.get("size", 0)
        size_mb = size_bytes / (1024 * 1024)
        if size_mb >= min_size_mb:
            candidates.append({"name": name, "size_mb": size_mb})

    if not candidates:
        return ModelSelectionResult()

    best = min(candidates, key=lambda m: m["size_mb"])
    return ModelSelectionResult(
        best_model=best["name"],
        best_size_mb=best["size_mb"],
        all_candidates=candidates,
    )


if __name__ == "__main__":
    import json
    import sys

    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    result = model_selector(data.get("models", []), data.get("min_size_mb", 0))
    print(json.dumps({
        "best_model": result.best_model,
        "best_size_mb": result.best_size_mb,
        "all_candidates": result.all_candidates,
    }, indent=2))
    sys.exit(0)
