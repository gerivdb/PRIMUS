# PRIMUS Registry — Registre des primitives
# IntentHash: 0xPRIMUS_REGISTRY_20260808
# ADR: ADR-2026-08-08-001-PRIMUS-CORE-REGISTRY

"""
Registre central des primitives PRIMUS.

Responsabilités:
- Charger les définitions YAML/JSON des primitives
- Indexer par nom, type, strate, priorité
- Fournir un accès immutable (frozen registry)
- Détecter les doublons et conflits de nom

Contrat:
  - Entrée: fichiers YAML/JSON dans primitives/ ou REGISTRY.yaml
  - Sortie: dict indexé + listes par catégorie
  - Effets de bord: aucun (lecture seule)
  - Dépendances: stdlib + loader.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


# ============================================================
# Types
# ============================================================

class PrimitiveType(str, Enum):
    """Catégories de primitives."""
    PARSER = "parser"
    VALIDATOR = "validator"
    TRANSFORMER = "transformer"
    EXECUTOR = "executor"
    FORMATTER = "formatter"


class Priority(str, Enum):
    """Niveaux de priorité."""
    P1 = "P1"  # Critique
    P2 = "P2"  # Important
    P3 = "P3"  # Standard


@dataclass(frozen=True, slots=True)
class PrimitiveDefinition:
    """
    Définition immutable d'une primitive PRIMUS.
    
    Charge depuis YAML/JSON via loader.py.
    """
    name: str
    version: str
    type: PrimitiveType
    strate: str
    priority: Priority
    input: Dict[str, Any] = field(default_factory=dict)
    output: Dict[str, Any] = field(default_factory=dict)
    tools: List[str] = field(default_factory=list)
    description: str = ""
    intent_hash: str = ""

    def __post_init__(self):
        if not self.name:
            raise ValueError("Primitive name cannot be empty")
        if not self.version:
            raise ValueError("Primitive version cannot be empty")


@dataclass
class RegistryStats:
    """Statistiques du registre."""
    total: int = 0
    by_type: Dict[str, int] = field(default_factory=dict)
    by_strate: Dict[str, int] = field(default_factory=dict)
    by_priority: Dict[str, int] = field(default_factory=dict)
    duplicates: List[str] = field(default_factory=list)


# ============================================================
# Registry
# ============================================================

class PrimitiveRegistry:
    """
    Registre immutable des primitives PRIMUS.
    
    Utilisation:
        registry = PrimitiveRegistry()
        registry.load_file("REGISTRY.yaml")
        registry.load_directory("primitives/")
        
        p = registry.get("workflow-runner")
        all_executors = registry.list_by_type(PrimitiveType.EXECUTOR)
    """

    def __init__(self) -> None:
        self._primitives: Dict[str, PrimitiveDefinition] = {}
        self._by_type: Dict[PrimitiveType, List[str]] = {
            t: [] for t in PrimitiveType
        }
        self._by_strate: Dict[str, List[str]] = {}
        self._by_priority: Dict[Priority, List[str]] = {
            p: [] for p in Priority
        }
        self._loaded_paths: Set[str] = set()

    # ---------------------------------------------------------
    # Chargement
    # ---------------------------------------------------------

    def load_file(self, path: Union[str, Path]) -> None:
        """
        Charge un fichier YAML/JSON de primitive.
        
        Args:
            path: Chemin vers le fichier YAML/JSON
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si la primitive est invalide ou en doublon
        """
        from .loader import load_primitive_file
        
        path_str = str(Path(path).resolve())
        if path_str in self._loaded_paths:
            return  # Déjà chargé
        
        primitive = load_primitive_file(path_str)
        self._register(primitive)
        self._loaded_paths.add(path_str)

    def load_directory(self, dir_path: Union[str, Path]) -> List[str]:
        """
        Charge tous les fichiers YAML/JSON d'un répertoire.
        
        Args:
            dir_path: Chemin du répertoire
            
        Returns:
            Liste des noms de primitives chargées
        """
        from .loader import load_primitive_directory
        
        return load_primitive_directory(dir_path, self._register)

    # ---------------------------------------------------------
    # Accès
    # ---------------------------------------------------------

    def get(self, name: str) -> PrimitiveDefinition:
        """
        Récupère une primitive par nom.
        
        Args:
            name: Nom de la primitive
            
        Returns:
            Définition de la primitive
            
        Raises:
            KeyError: Si la primitive n'existe pas
        """
        if name not in self._primitives:
            raise KeyError(f"Primitive '{name}' not found in registry")
        return self._primitives[name]

    def list_all(self) -> List[PrimitiveDefinition]:
        """Liste toutes les primitives (ordre alphabétique)."""
        return sorted(self._primitives.values(), key=lambda p: p.name)

    def list_by_type(self, ptype: PrimitiveType) -> List[PrimitiveDefinition]:
        """Liste les primitives d'un type donné."""
        names = self._by_type.get(ptype, [])
        return [self._primitives[n] for n in names if n in self._primitives]

    def list_by_strate(self, strate: str) -> List[PrimitiveDefinition]:
        """Liste les primitives d'une strate donnée."""
        names = self._by_strate.get(strate, [])
        return [self._primitives[n] for n in names if n in self._primitives]

    def list_by_priority(self, priority: Priority) -> List[PrimitiveDefinition]:
        """Liste les primitives d'une priorité donnée."""
        names = self._by_priority.get(priority, [])
        return [self._primitives[n] for n in names if n in self._primitives]

    def has(self, name: str) -> bool:
        """Vérifie si une primitive existe dans le registre."""
        return name in self._primitives

    def __contains__(self, name: str) -> bool:
        return self.has(name)

    def __len__(self) -> int:
        return len(self._primitives)

    # ---------------------------------------------------------
    # Stats
    # ---------------------------------------------------------

    def stats(self) -> RegistryStats:
        """Retourne les statistiques du registre."""
        stats = RegistryStats(total=len(self._primitives))
        
        for p in self._primitives.values():
            stats.by_type[p.type.value] = stats.by_type.get(p.type.value, 0) + 1
            stats.by_strate[p.strate] = stats.by_strate.get(p.strate, 0) + 1
            stats.by_priority[p.priority.value] = stats.by_priority.get(p.priority.value, 0) + 1
        
        return stats

    # ---------------------------------------------------------
    # Internes
    # ---------------------------------------------------------

    def _register(self, primitive: PrimitiveDefinition) -> None:
        """Enregistre une primitive (vérifie doublons)."""
        if primitive.name in self._primitives:
            existing = self._primitives[primitive.name]
            raise ValueError(
                f"Duplicate primitive '{primitive.name}': "
                f"existing version={existing.version}, new version={primitive.version}"
            )
        
        self._primitives[primitive.name] = primitive
        self._by_type[primitive.type].append(primitive.name)
        
        if primitive.strate not in self._by_strate:
            self._by_strate[primitive.strate] = []
        self._by_strate[primitive.strate].append(primitive.name)
        
        self._by_priority[primitive.priority].append(primitive.name)


# ============================================================
# Helpers
# ============================================================

def create_registry_from_paths(paths: List[Union[str, Path]]) -> PrimitiveRegistry:
    """
    Crée un registry depuis une liste de chemins (fichiers ou répertoires).
    
    Args:
        paths: Liste de chemins vers des fichiers YAML/JSON ou répertoires
        
    Returns:
        PrimitiveRegistry peuplé
    """
    registry = PrimitiveRegistry()
    for path in paths:
        p = Path(path)
        if p.is_file():
            registry.load_file(p)
        elif p.is_dir():
            registry.load_directory(p)
    return registry


# ============================================================
# EXPORTS PUBLICS
# ============================================================

__all__ = [
    'PrimitiveType',
    'Priority',
    'PrimitiveDefinition',
    'RegistryStats',
    'PrimitiveRegistry',
    'create_registry_from_paths',
]
