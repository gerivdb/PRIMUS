# ⚛️ PRIMUS — Primitive Executable Atoms

> Blocs atomiques exécutables. Stateless. Single-responsibility. Testables en 1 assertion.
> Consommés par CTULU (tools), SKILLS (skills cognitifs) et NEXUS (engines).

---

## Principe

Une primitive PRIMUS répond à **une seule question**, ne dépend d'aucun contexte extérieur, et retourne toujours le même output pour le même input.

```
PRIMUS    → atome     (1 responsabilité, < 100 lignes, 0 état)
CTULU     → molécule  (assemble des primitives pour un usage multi-repo)
SKILLS    → skill     (orchestre tools + primitives avec contexte cognitif)
NEXUS     → engine    (logique métier, consomme primitives + tools)
```

---

## Structure

```
primitives/
  parsing/        # parsers atomiques (JSON, YAML, Markdown, repo tree)
  comparison/     # comparators (diff, similarity, jurisdiction check)
  formatting/     # formatters (report, table, ADR, markdown)
  validation/     # validators (schema, type, contract)
  deduction/      # inférence atomique (eligibility, classification)
pipelines/        # compositions de primitives en séquences déclaratives
schemas/          # contrats d'interface (input/output par primitive)
tests/            # 1 test par primitive, couverture 100% obligatoire
```

---

## Contrat d'une primitive

Chaque primitive doit respecter :
- **Input** : typé, documenté dans `schemas/`
- **Output** : typé, déterministe
- **Effets de bord** : aucun
- **Dépendances** : uniquement d'autres primitives PRIMUS ou stdlib
- **Tests** : au moins 1 test unitaire dans `tests/`
- **Taille** : < 100 lignes (sinon → candidat CTULU tool)

---

## Relation avec les autres repos

| Repo | Relation avec PRIMUS |
|---|---|
| **CTULU** | Consomme PRIMUS pour construire des tools multi-repo |
| **SKILLS** | Appelle des primitives PRIMUS directement dans les skills cognitifs |
| **NEXUS** | Importe des primitives PRIMUS dans les engines métier |
| **ONTOLOGY/primitives/** | Contient les *specs déclaratives* (YAML) dont PRIMUS est l'implémentation |
| **DevTools** | N'importe pas PRIMUS — niveau infra, pas logique |

---

## Ce que PRIMUS n'est PAS

- ❌ Pas un SDK (pas de façade haut niveau)
- ❌ Pas un framework (n'impose aucune convention d'exécution)
- ❌ Pas un outil ops (pas de CLI, pas de runner)
- ❌ Pas une copie d'ONTOLOGY/primitives/ (ONTOLOGY = specs, PRIMUS = code)

---

## Références

- [ONTOLOGY — PRIMUS_ARCHITECTURE.md](https://github.com/gerivdb/ONTOLOGY/blob/main/PRIMUS_ARCHITECTURE.md)
- [GOVERNANCE-HUB — ADR_PRIMUS_VS_CTULU.md](https://github.com/gerivdb/GOVERNANCE-HUB/blob/main/ADR_PRIMUS_VS_CTULU.md)
- [ONTOLOGY — DEVTOOLS_VS_CTULU_JURISDICTION.md](https://github.com/gerivdb/ONTOLOGY/blob/main/DEVTOOLS_VS_CTULU_JURISDICTION.md)

---

*gerivdb/PRIMUS — 2026-06-10*
