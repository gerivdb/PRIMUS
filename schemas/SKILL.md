---
name: primus-schemas
description: "Contrats de schéma Primus (json_schema_validator, primitive_contract, repo_tree_parser, text_line_parser, yaml_parser). Dossier de schémas Primus, pas un skill KiloCode canonique."
version: 1.0.0
intent_hash: 0xPRIMUS_SCHEMAS_20261124
gericode_version: "1.0"
stratum: L4-TOOLS
shard_id: G
turn_counter: 1
uuid: primus-schemas-001
timestamp: "2026-11-24T03:30:00Z"
invariants:
  friction: 0.0
  entropy: 0.0
wal_reference: "WAL-0x243-PRIMUS-SCHEMAS-001"
---

# primus-schemas

## Rôle

Dossier contenant les contrats de schéma JSON du système Primus. Ce n'est **pas** un skill KiloCode canonique invoquable via `skill-router.ps1`, mais un ensemble de fichiers de schéma utilisés pour valider la structure des données dans l'écosystème gerivdb.

## Contenu

| Fichier | Rôle |
|---------|------|
| `json_schema_validator.contract.json` | Schéma de validation JSON générique |
| `primitive_contract.schema.json` | Contrat des primitives Primus |
| `repo_tree_parser.contract.json` | Contrat du parser d'arbre de repo |
| `text_line_parser.contract.json` | Contrat du parser de lignes de texte |
| `yaml_parser.contract.json` | Contrat du parser YAML |

## Dépendances

- Aucun (fichiers de schéma statiques)

## Antipatterns bloqués

- Invoquer `primus-schemas` comme un skill KiloCode (ce n'est pas un skill, c'est un dossier de schémas)
- Modifier un schéma sans mettre à jour les validateurs qui l'utilisent
