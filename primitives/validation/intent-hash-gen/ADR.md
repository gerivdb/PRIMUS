---
type: ADR
status: proposed
date: "2026-08-19"
intent_hash: 0xADR_PRIMITIVE_INTENT_HASH_GEN_20260819
---

# ADR-2026-08-19-PRIMITIVE-INTENT-HASH-GEN -- Primitive de génération d'IntentHash

## Contexte

La génération d'IntentHash est manuelle (copier-coller de slug).
Risques :
- Erreur humaine (typo, casse)
- Collisions non détectées
- Pas de format validation

## Décision

Créer la primitive `intent-hash-gen` dans L4-TOOLS/PRIMUS/primitives/validation/ :

**Responsabilité** : générer un IntentHash valide et unique :
- Input : slug humain (ex: "INTENT-MCP-SYNAPTIC-ECOSYSTEM-VISION-20260819_v10")
- Output : hash format `0xSLUG_MAJUSCULES`
- Collision detection : scan de INTENTS/ pour vérifier unicité
- Side effects : aucun
- Dependencies : stdlib uniquement

**Structure** :
- `intent_hash_gen.py` : implémentation
- `README.md` : documentation

## Conséquences

- IntentHash fiables, pas de collision
- Format garanti : `0x[A-Z0-9_-]+`
- Traçabilité dans WAL

## Référence

- **ADR** : ADR-2026-08-19-PRIMITIVE-INTENT-HASH-GEN
- **IntentHash** : 0xADR_PRIMITIVE_INTENT_HASH_GEN_20260819
- **Dépôt** : gerivdb/PRIMUS
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded
