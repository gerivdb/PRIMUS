---
name: primus-primitives
description: "Briques primitives du système Primus (comparaison, contributions, core, deduction, detectors, formatting, logic, parsing, validation). Dossier de code Primus, pas un skill KiloCode canonique."
version: 1.0.0
intent_hash: 0xPRIMUS_PRIMITIVES_20261124
gericode_version: "1.0"
stratum: L4-TOOLS
shard_id: G
turn_counter: 1
uuid: primus-primitives-001
timestamp: "2026-11-24T03:30:00Z"
invariants:
  friction: 0.0
  entropy: 0.0
wal_reference: "WAL-0x243-PRIMUS-PRIMITIVES-001"
---

# primus-primitives

## Rôle

Dossier de code Primus contenant les briques primitives du système. Ce n'est **pas** un skill KiloCode canonique invoquable via `skill-router.ps1`, mais un ensemble de modules Python réutilisables par les skills et citoyens de l'écosystème gerivdb.

## Contenu

| Sous-dossier | Rôle |
|-------------|------|
| `comparison` | Opérateurs de comparaison et diff |
| `contributions` | Contributions au système Primus |
| `core` | Cœur du système Primus |
| `deduction` | Moteurs de déduction |
| `detectors` | Détecteurs d'anomalies et patterns |
| `formatting` | Formatage de sortie |
| `logic` | Opérateurs logiques |
| `parsing` | Parsers de formats variés |
| `validation` | Validateurs de schémas et données |

## Dépendances

- `primus-schemas` : contrats de schéma pour validation
- `primus-skills` : skills d'interface Primus

## Antipatterns bloqués

- Invoquer `primus-primitives` comme un skill KiloCode (ce n'est pas un skill, c'est un dossier de code)
- Modifier un fichier sans test unitaire associé
