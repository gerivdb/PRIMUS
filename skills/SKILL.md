---
name: primus-skills
description: "Skills d'interface Primus (contributions). Dossier de skills Primus, pas un skill KiloCode canonique."
version: 1.0.0
intent_hash: 0xPRIMUS_SKILLS_20261124
gericode_version: "1.0"
stratum: L4-TOOLS
shard_id: G
turn_counter: 1
uuid: primus-skills-001
timestamp: "2026-11-24T03:30:00Z"
invariants:
  friction: 0.0
  entropy: 0.0
wal_reference: "WAL-0x243-PRIMUS-SKILLS-001"
---

# primus-skills

## Rôle

Dossier contenant les skills d'interface du système Primus. Ce n'est **pas** un skill KiloCode canonique invoquable via `skill-router.ps1`, mais un ensemble de skills spécifiques à Primus réutilisables dans l'écosystème gerivdb.

## Contenu

| Sous-dossier | Rôle |
|-------------|------|
| `contributions` | Skills de contribution Primus |

## Dépendances

- `primus-primitives` : briques primitives du système
- `primus-schemas` : contrats de schéma

## Antipatterns bloqués

- Invoquer `primus-skills` comme un skill KiloCode (ce n'est pas un skill, c'est un dossier de skills Primus)
- Modifier un skill Primus sans test unitaire associé
