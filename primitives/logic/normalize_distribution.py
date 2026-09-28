#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : normalize_distribution
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Normalise une distribution de probabilités.
"""
from __future__ import annotations


def normalize_distribution(probabilities: list[float]) -> list[float]:
    """Normalise la liste pour que la somme vaille 1."""
    total = sum(probabilities)
    if total <= 0:
        raise ValueError("probabilities must have a positive sum")
    return [p / total for p in probabilities]
