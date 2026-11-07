#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : text_line_parser
Catégorie : parsing
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Parse un contenu texte en lignes non vides et non commentées.

Contrat :
  - Input  : content: str, comment_char: str = "#", strip: bool = True
  - Output : List[str] (lignes non vides, non commentées)
  - Effets de bord : aucun
  - Dépendances : stdlib uniquement
"""

from typing import List


def text_line_parser(
    content: str,
    comment_char: str = "#",
    strip: bool = True,
) -> List[str]:
    """Extrait les lignes non vides et non commentées d'un contenu texte.

    Args:
        content: Contenu texte brut.
        comment_char: Caractère indiquant un commentaire (défaut "#").
        strip: Supprimer les espaces en début/fin de ligne (défaut True).

    Returns:
        Liste des lignes filtrées.
    """
    result: List[str] = []
    for line in content.splitlines():
        if strip:
            line = line.strip()
        if not line:
            continue
        if line.startswith(comment_char):
            continue
        result.append(line)
    return result
