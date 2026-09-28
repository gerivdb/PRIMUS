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
| **JEVX** | Source de primitives `validation` et `logic` importées comme `reference_impl` |
| **localjev-upstream** | Source de primitives `logic` importées comme `reference_impl` |

---

## Primitives importées

### Depuis JEVX (`validation`)

| Primitive | Fichier | Description |
|---|---|---|
| `gitignore-audit` | `primitives/validation/gitignore_audit.py` | Audit .gitignore d'un dépôt git |
| `mcp-scope-check` | `primitives/validation/mcp_scope_check.py` | Vérifie la portée MCP/shell d'un chemin |
| `tool-schema-validator` | `primitives/validation/tool_schema_validator.py` | Valide les paramètres d'appels outils |
| `yaml-editor` | `primitives/validation/yaml_editor.py` | Édition YAML sécurisée |

### Depuis JEVX (`logic`)

| Primitive | Fichier | Description |
|---|---|---|
| `benchmark-latency` | `primitives/logic/benchmark_latency.py` | Mesure la latence d'un endpoint HTTP |
| `entropy-monitor` | `primitives/logic/entropy_monitor.py` | Calcule l'entropie d'une distribution |
| `generate-validation-report` | `primitives/logic/generate_validation_report.py` | Génère un rapport de validation |
| `integration-score` | `primitives/logic/integration_score.py` | Calcule un score d'intégration global |
| `model-selector` | `primitives/logic/model_selector.py` | Sélectionne le meilleur modèle candidat |
| `service-lifecycle` | `primitives/logic/service_lifecycle.py` | Valide un manifeste de services |

### Depuis localjev-upstream (`logic`)

| Primitive | Fichier | Description |
|---|---|---|
| `confidence` | `primitives/logic/confidence.py` | Calcule la confiance d'une distribution |
| `normalize-distribution` | `primitives/logic/normalize_distribution.py` | Normalise une distribution de probabilités |
| `prepare-questions` | `primitives/logic/prepare_questions.py` | Prépare les questions pour l'inférence |
| `build-output-schema` | `primitives/logic/build_output_schema.py` | Construit le schéma de sortie JSON |
| `decode-answers` | `primitives/logic/decode_answers.py` | Décode les réponses brutes |
| `extract-json` | `primitives/logic/extract_json.py` | Extrait un objet JSON d'une chaîne brute |
| `validate-system-one-request` | `primitives/logic/validate_system_one_request.py` | Valide une requête System-1 |

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
