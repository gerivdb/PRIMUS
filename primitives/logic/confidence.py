#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : confidence
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Calcule la confiance d'une distribution de probabilités.
"""
from __future__ import annotations

import math


def confidence(probabilities: list[float]) -> float:
    """Retourne la confiance normalisée entre 0 et 1."""
    entropy = -sum(
        p * math.log(p) for p in probabilities if p > 0
    )
    value = 1 - entropy / math.log(len(probabilities))
    return max(0.0, min(1.0, value))
