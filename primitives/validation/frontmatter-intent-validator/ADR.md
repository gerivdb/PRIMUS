---
type: ADR
status: proposed
date: "2026-08-19"
intent_hash: 0xADR_PRIMITIVE_FRONTMATTER_INTENT_VALIDATOR_20260819
---

# ADR-2026-08-19-PRIMITIVE-FRONTMATTER-INTENT-VALIDATOR -- Validation frontmatter INTENT

## Contexte

`frontmatter-guardian` existe en skill global, mais pas de primitive PRIMUS
dédiée à la validation spécifique des INTENTs :
- IntentHash format
- Status/priority values
- Sections requises (1, 2, 3, 4, 5, 6, 10, 27)

## Décision

Créer la primitive `frontmatter-intent-validator` dans PRIMUS :

**Responsabilité** : valider frontmatter + sections d'un INTENT :
- intent_hash format `0x[A-Za-z0-9_-]+`
- status ∈ {proposed, accepted, deprecated, superseded, archived}
- priority ∈ {P0, P1, P2, P3}
- sections requises présentes

**Structure** :
- `frontmatter_intent_validator.py` : implémentation
- `README.md` : documentation

## Conséquences

- Validation automatique avant commit
- Pas de bypass possible du format IntentHash
- Garantie de conformité structurelle

## Référence

- **ADR** : ADR-2026-08-19-PRIMITIVE-FRONTMATTER-INTENT-VALIDATOR
- **IntentHash** : 0xADR_PRIMITIVE_FRONTMATTER_INTENT_VALIDATOR_20260819
- **Dépôt** : gerivdb/PRIMUS
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded
