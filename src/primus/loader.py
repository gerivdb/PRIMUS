# PRIMUS Loader — Chargement YAML/JSON des primitives
# IntentHash: 0xPRIMUS_LOADER_20260808
# ADR: ADR-2026-08-08-001-PRIMUS-CORE-REGISTRY

"""
Loader de définitions de primitives PRIMUS depuis YAML ou JSON.

Responsabilités:
- Charger un fichier YAML/JSON unique
- Charger un répertoire récursivement
- Valider les champs obligatoires
- Convertir en PrimitiveDefinition (dataclass immutable)

Contrat:
  - Entrée: chemin fichier ou répertoire
  - Sortie: PrimitiveDefinition ou liste de PrimitiveDefinition
  - Effets de bord: lecture fichiers uniquement
  - Dépendances: stdlib (json, pathlib) + PyYAML (optionnel)
"""

from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

from .registry import PrimitiveDefinition, PrimitiveType, Priority


# ============================================================
# Constantes
# ============================================================

SUPPORTED_EXTENSIONS = {".yaml", ".yml", ".json"}
REQUIRED_FIELDS = {"name", "version", "type", "strate", "priority"}


# ============================================================
# Exceptions
# ============================================================

class PrimitiveLoadError(Exception):
    """Erreur de chargement d'une primitive."""
    pass


class PrimitiveValidationError(Exception):
    """Erreur de validation d'une primitive."""
    pass


# ============================================================
# Chargement fichier unique
# ============================================================

def load_primitive_file(path: str) -> PrimitiveDefinition:
    """
    Charge un fichier YAML/JSON de primitive.
    
    Args:
        path: Chemin absolu vers le fichier
        
    Returns:
        PrimitiveDefinition
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        PrimitiveLoadError: Si le format est invalide
        PrimitiveValidationError: Si les champs obligatoires sont manquants
    """
    file_path = Path(path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Primitive file not found: {path}")
    
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise PrimitiveLoadError(
            f"Unsupported file extension: {file_path.suffix}. "
            f"Supported: {SUPPORTED_EXTENSIONS}"
        )
    
    # Lecture selon extension
    raw = _read_file(file_path)
    
    # Parsing YAML ou JSON
    data = _parse_content(raw, file_path.suffix)
    
    # Validation
    _validate_primitive_data(data, path)
    
    # Conversion en PrimitiveDefinition
    return _to_primitive_definition(data)


def load_primitive_directory(
    dir_path: Union[str, Path],
    register_callback: Callable[[PrimitiveDefinition], None],
) -> List[str]:
    """
    Charge récursivement toutes les primitives d'un répertoire.
    
    Args:
        dir_path: Chemin du répertoire
        register_callback: Fonction appelée pour chaque primitive chargée
        
    Returns:
        Liste des noms de primitives chargées
    """
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        raise PrimitiveLoadError(f"Not a directory: {dir_path}")
    
    loaded_names: List[str] = []
    
    for root, _, files in os.walk(dir_path):
        for filename in sorted(files):
            file_path = Path(root) / filename
            if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            
            try:
                primitive = load_primitive_file(str(file_path))
                register_callback(primitive)
                loaded_names.append(primitive.name)
            except (PrimitiveLoadError, PrimitiveValidationError) as e:
                # Skip fichiers invalides mais continue le scan
                import warnings
                warnings.warn(f"Failed to load {file_path}: {e}")
    
    return loaded_names


# ============================================================
# Lecture fichiers
# ============================================================

def _read_file(file_path: Path) -> str:
    """Lit un fichier texte (UTF-8)."""
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise PrimitiveLoadError(f"Invalid UTF-8 encoding: {file_path}")


def _parse_content(content: str, extension: str) -> Dict[str, Any]:
    """Parse le contenu YAML ou JSON en dict."""
    if extension.lower() in {".yaml", ".yml"}:
        return _parse_yaml(content)
    else:
        return _parse_json(content)


def _parse_yaml(content: str) -> Dict[str, Any]:
    """Parse YAML vers dict."""
    try:
        import yaml
        return yaml.safe_load(content) or {}
    except ImportError:
        # Fallback: parsing YAML minimaliste
        return _parse_yaml_fallback(content)
    except yaml.YAMLError as e:
        raise PrimitiveLoadError(f"Invalid YAML: {e}")


def _parse_yaml_fallback(content: str) -> Dict[str, Any]:
    """
    Parser YAML minimaliste (sans PyYAML).
    
    Gère les cas simples: clés scalaires, listes, dicts imbriqués.
    """
    result: Dict[str, Any] = {}
    current_section = result
    current_path: List[str] = []
    in_list = False
    
    for line in content.split("\n"):
        stripped = line.strip()
        
        # Skip commentaires et lignes vides
        if not stripped or stripped.startswith("#"):
            continue
        
        # Détection liste
        if stripped.startswith("- "):
            if not in_list:
                in_list = True
            item = stripped[2:].strip()
            # Handle nested dicts in lists
            if ":" in item:
                key, _, value = item.partition(":")
                current_section.append({key.strip(): _coerce_value(value.strip())})
            else:
                current_section.append(_coerce_value(item))
            continue
        
        in_list = False
        
        # Détection clé:valeur
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            
            # Détection indentation (changement de section)
            indent = len(line) - len(line.lstrip())
            while current_path and indent <= _get_indent(current_path[-1], content):
                current_path.pop()
                if current_path:
                    current_section = _navigate(result, current_path)
            
            if not value:
                # Nouvelle section imbriquée
                current_path.append((key, indent))
                current_section[key] = {}
                current_section = current_section[key]
            else:
                current_section[key] = _coerce_value(value)
    
    return result


def _coerce_value(value: str) -> Any:
    """Convertit une string YAML vers le type Python approprié."""
    if not value or value == "null" or value == "~":
        return None
    if value in {"true", "True", "yes", "Yes"}:
        return True
    if value in {"false", "False", "no", "No"}:
        return False
    # Tentative int/float
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        pass
    # Tentative list
    if value.startswith("[") and value.endswith("]"):
        items = value[1:-1].split(",")
        return [_coerce_value(item.strip()) for item in items if item.strip()]
    # String (déjà quotes ou pas)
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def _get_indent(key: str, content: str) -> int:
    """Trouve l'indentation d'une clé dans le contenu."""
    for line in content.split("\n"):
        if line.strip().startswith(key + ":"):
            return len(line) - len(line.lstrip())
    return 0


def _navigate(data: Dict[str, Any], path: List[tuple]) -> Dict[str, Any]:
    """Navigue dans un dict imbriqué selon un chemin de clés."""
    current = data
    for key, _ in path:
        current = current[key]
    return current


def _parse_json(content: str) -> Dict[str, Any]:
    """Parse JSON vers dict."""
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise PrimitiveLoadError(f"Invalid JSON: {e}")


# ============================================================
# Validation
# ============================================================

def _validate_primitive_data(data: Dict[str, Any], path: str) -> None:
    """
    Valide les champs obligatoires d'une primitive.
    
    Champs requis:
    - name: str
    - version: str
    - type: str (parser|validator|transformer|executor|formatter)
    - strate: str
    - priority: str (P1|P2|P3)
    """
    missing = REQUIRED_FIELDS - set(data.keys())
    if missing:
        raise PrimitiveValidationError(
            f"Missing required fields in {path}: {missing}"
        )
    
    # Validation type
    try:
        PrimitiveType(data["type"])
    except ValueError:
        raise PrimitiveValidationError(
            f"Invalid type '{data['type']}' in {path}. "
            f"Allowed: {[t.value for t in PrimitiveType]}"
        )
    
    # Validation priority
    try:
        Priority(data["priority"])
    except ValueError:
        raise PrimitiveValidationError(
            f"Invalid priority '{data['priority']}' in {path}. "
            f"Allowed: {[p.value for p in Priority]}"
        )


# ============================================================
# Conversion
# ============================================================

def _to_primitive_definition(data: Dict[str, Any]) -> PrimitiveDefinition:
    """
    Convertit un dict YAML/JSON en PrimitiveDefinition.
    
    Args:
        data: Données parsées
        
    Returns:
        PrimitiveDefinition immutable
    """
    return PrimitiveDefinition(
        name=data["name"],
        version=str(data["version"]),
        type=PrimitiveType(data["type"]),
        strate=str(data["strate"]),
        priority=Priority(data["priority"]),
        input=data.get("input", {}),
        output=data.get("output", {}),
        tools=data.get("tools", []),
        description=data.get("description", ""),
        intent_hash=data.get("intent_hash", ""),
    )


# ============================================================
# EXPORTS PUBLICS
# ============================================================

__all__ = [
    'PrimitiveLoadError',
    'PrimitiveValidationError',
    'load_primitive_file',
    'load_primitive_directory',
]
