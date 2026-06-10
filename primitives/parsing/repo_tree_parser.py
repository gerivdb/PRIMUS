#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : repo_tree_parser
Catégorie : parsing
Spec      : ONTOLOGY/primitives/ (voir schema ci-dessous)

Responsabilité unique :
  Parse la structure d'arbre d'un repo GitHub (liste de dicts GitHub API
  ou liste de chemins strings) en un dict hiérarchique imbriquié.

Contrat :
  - Input  : List[Dict] (réponse GitHub contents API) OU List[str] (chemins)
  - Output : Dict  {name, type, path, children[]}
  - Stateless : oui
  - Effets de bord : aucun
  - Dépendances : stdlib uniquement
"""
from __future__ import annotations
from typing import Any, Dict, List, Union


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

TreeNode = Dict[str, Any]
# {
#   "name"    : str,
#   "type"    : "file" | "dir",
#   "path"    : str,
#   "children": List[TreeNode]   # vide si type == "file"
# }


# ---------------------------------------------------------------------------
# Primitive
# ---------------------------------------------------------------------------

def repo_tree_parser(
    entries: Union[List[Dict[str, Any]], List[str]],
) -> Dict[str, Any]:
    """
    Parse une liste d'entrées repo en arbre hiérarchique.

    Args:
        entries: soit une liste de dicts GitHub API
                 (avec clés "path", "type" optionnel)
                 soit une liste de chemins strings ("src/foo/bar.py")

    Returns:
        Dict root avec clé "children" contenant l'arbre imbriqué.
        Chaque nœud : {name, type, path, children}
    """
    paths = _normalize(entries)
    root: TreeNode = {"name": "", "type": "dir", "path": "", "children": []}
    for path, ftype in paths:
        _insert(root, path.split("/"), path, ftype)
    return root


def flatten_tree(root: Dict[str, Any]) -> List[str]:
    """
    Utilitaire complémentaire : aplatit un arbre en liste de chemins.
    Stateless. Pas d'effets de bord.
    """
    result: List[str] = []
    _flatten(root, result)
    return result


def find_in_tree(root: Dict[str, Any], name: str) -> List[TreeNode]:
    """
    Recherche par nom dans l'arbre (recherche en profondeur).
    Retourne tous les nœuds dont le nom correspond exactement.
    Stateless. Pas d'effets de bord.
    """
    results: List[TreeNode] = []
    _search(root, name, results)
    return results


# ---------------------------------------------------------------------------
# Helpers internes
# ---------------------------------------------------------------------------

def _normalize(
    entries: Union[List[Dict[str, Any]], List[str]]
) -> List[tuple]:
    """Normalise en liste de (path_str, type_str)."""
    if not entries:
        return []
    if isinstance(entries[0], str):
        return [(e.strip("/"), "file") for e in entries if e.strip("/")]
    result = []
    for e in entries:
        path = e.get("path", "").strip("/")
        ftype = e.get("type", "file")  # "file" | "dir"
        if path:
            result.append((path, ftype))
    return result


def _insert(
    node: TreeNode,
    parts: List[str],
    full_path: str,
    ftype: str,
) -> None:
    """Insère récursivement un chemin dans l'arbre."""
    if not parts:
        return
    name = parts[0]
    # Cherche si l'enfant existe déjà
    child = next((c for c in node["children"] if c["name"] == name), None)
    if child is None:
        is_leaf = len(parts) == 1
        child = {
            "name": name,
            "type": ftype if is_leaf else "dir",
            "path": full_path if is_leaf else "/".join(full_path.split("/")[: full_path.split("/").index(name) + 1]),
            "children": [],
        }
        node["children"].append(child)
    if len(parts) > 1:
        _insert(child, parts[1:], full_path, ftype)


def _flatten(node: TreeNode, acc: List[str]) -> None:
    if node["path"]:
        acc.append(node["path"])
    for child in node.get("children", []):
        _flatten(child, acc)


def _search(node: TreeNode, name: str, acc: List[TreeNode]) -> None:
    if node["name"] == name:
        acc.append(node)
    for child in node.get("children", []):
        _search(child, name, acc)
