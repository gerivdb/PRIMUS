# CTULU IO Types — 11 types d'artefacts
# IntentHash: 0xCTULU_IO_TYPES_20260808
# ADR: ADR-2026-08-08-001-PRIMUS-CORE-REGISTRY

## Vue d'ensemble

CTULU utilise 11 types d'artefacts stricts pour les entrées/sorties des
primitives. Ce contrat garantit l'interopérabilité entre les couches
N+1 (GOVERNANCE-HUB), N+2 (ARGUS/TRIX), N+3 (CTULU/BRAIN/FLUENCE) et
N+4 (ECOS-CLI).

## Les 11 types

| # | Type | Description | Exemple |
|---|------|-------------|---------|
| 1 | `primitive` | Définition YAML d'une primitive | REGISTRY.yaml |
| 2 | `wave` | Onde ternaire (band + trit + phase + amplitude) | WaveArray 81 slots |
| 3 | `trit` | Valeur ternaire {-1, 0, +1} | Trit.POS, Trit.NEG, Trit.ZERO |
| 4 | `tree` | Arbre hiérarchique imbriqué | repo_tree_parser output |
| 5 | `graph` | Graphe (DAG-3, DOT, Mermaid) | dag3_parser output |
| 6 | `config` | Configuration JSON/YAML | gate_config, ascii_map |
| 7 | `report` | Rapport de validation/audit | cycles, symmetry, cardinality |
| 8 | `intent_hash` | Hash d'intention (0x...) | 0xPRIMUS_CORE_PRIMITIVE_20260808 |
| 9 | `matrix` | Matrice ternaire 81x81 | SparseRolling, ExaGEMM |
| 10 | `wal` | Write-Ahead Log entry | WAL entry JSON |
| 11 | `artifact` | Artefact binaire/générique | b64 encoded, binary blob |

## Détails par type

### 1. primitive
Définition YAML d'une primitive PRIMUS.

```yaml
name: workflow-runner
version: "1.0.0"
type: executor
strate: L4
priority: P1
input: {...}
output: {...}
tools: [...]
```

### 2. wave
Onde ternaire complète.

```python
from dataclasses import dataclass
from primus.core.types import Wave, FrequencyBand, Trit

w: Wave = Wave(
    band=FrequencyBand.ALPHA,
    trit=Trit.POS,
    phase=0.0,
    amplitude=1.0
)
```

### 3. trit
Valeur ternaire signée.

```python
from primus.core.types import Trit

t: Trit = Trit.POS  # -1, 0, ou +1
```

### 4. tree
Arbre hiérarchique imbriqué.

```python
TreeNode = Dict[str, Any]  # {name, type, path, children[]}
root: TreeNode = {"name": "", "type": "dir", "path": "", "children": [...]}
```

### 5. graph
Graphe (DAG-3, DOT, Mermaid).

```python
# DAG-3
GraphDict = Dict[str, Any]  # {nodes: [...], edges: [...]}
```

### 6. config
Configuration JSON/YAML.

```python
ConfigDict = Dict[str, Any]  # gate_config, ascii_map, etc.
```

### 7. report
Rapport de validation/audit.

```python
ReportDict = Dict[str, Any]  # {status, errors, warnings, details}
```

### 8. intent_hash
Hash d'intention (0x...).

```python
IntentHash = str  # Format: 0xSLUG_MAJUSCULES_YYYYMMDD
```

### 9. matrix
Matrice ternaire 81x81.

```python
from primus.core.types import WaveArray
matrix: WaveArray  # 81 ondes = 81 slots (9 bandes x 9 positions)
```

### 10. wal
Write-Ahead Log entry.

```python
WALEntry = Dict[str, Any]  # {id, action, timestamp, payload, status}
```

### 11. artifact
Artefact binaire/générique.

```python
Artifact = bytes  # Contenu binaire encodé (base64, raw)
```

## Règles de flux

1. Toute entrée/sortie de primitive DOIT utiliser un de ces 11 types
2. Les types composés (`wave`, `tree`, `graph`, `matrix`) sont immutables
3. Les types `report` et `wal` sont append-only (jamais modifiés)
4. Le type `config` est le seul mutable (reconfigurations autorisées)

## Référence ADR
- **ADR** : ADR-2026-08-08-001-PRIMUS-CORE-REGISTRY
- **IntentHash** : 0xCTULU_IO_TYPES_20260808
- **Dépôt** : gerivdb/PRIMUS
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded
