# Primitive Atomique PRIMUS
# IntentHash: 0xPRIMUS_CORE_PRIMITIVE_20260808
# ADR: ADR-2026-08-08-001-PRIMUS-CORE-REGISTRY

## Définition

Une **primitive PRIMUS** est l'unité atomique de comportement dans l'écosystème
L4-TOOLS. Elle encapsule une responsabilité unique, sans état global, avec un
contrat d'entrée/sortie strict.

## Contrat (obligatoire)

| Aspect | Règle |
|--------|-------|
| Responsabilité | UNIQUE — une primitive = un comportement |
| État | Stateless — aucun état global, pas de singleton |
| Entrée | Types explicites (voir CTULU_IO_TYPES.md) |
| Sortie | Types explicites — never `Any` en sortie |
| Effets de bord | Documentés — `None` si absents |
| Dépendances | stdlib uniquement, ou dépendances déclarées |
| Idempotence | `f(x) == f(x)` garanti |

## Structure d'une primitive

```yaml
# Exemple minimal
name: ma-primitive
version: "1.0.0"
type: parser  # parser | validator | transformer | executor | formatter
strate: L4
priority: P1

input:
  data:
    type: object
    description: "Entrée attendue"

output:
  result:
    type: object
    description: "Sortie produite"

tools:
  - nom-outil-1
  - nom-outil-2
```

## Règles d'implémentation

1. **Un fichier = une primitive** (ou un module Python avec fonctions pures)
2. **Pas de classes avec état mutable** — préférer les dataclasses `frozen=True`
3. **Typage strict** — pas de `# type: ignore` sans ADR
4. **Documentation inline** — docstring sur toute fonction publique
5. **Tests unitaires** — un fichier `tests/test_<nom_primitive>.py` par primitive

## Catégories de primitives

| Catégorie | Rôle | Exemples |
|-----------|------|----------|
| parsing | Lecture/transformation de structure | repo_tree_parser, dag3_parser |
| validation | Vérification de contraintes | json_schema_validator, cycles |
| formatting | Sortie/rendu | ascii_graph, dot_graph, mermaid_graph |
| deduction | Analyse/impact | i_score, impact, transitive |
| comparison | Diff/regard | cache_key, graph_diff |
| narrative | TALEX/ storytelling | dag3, gridnet, intent_hash |
| executor | Exécution de workflows | step_executor, workflow-runner |

## Référence ADR
- **ADR** : ADR-2026-08-08-001-PRIMUS-CORE-REGISTRY
- **IntentHash** : 0xPRIMUS_CORE_PRIMITIVE_20260808
- **Dépôt** : gerivdb/PRIMUS
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded
