# workflow-anything — Processus multi-étapes déclarés

## Description

Moteur de workflows multi-étapes déclarés en YAML. Orchestre les outils
CTULU en séquences avec dépendances, validation, et visualisation Mermaid.

## Usage

```bash
workflow-anything create   --name my-workflow --template standard
workflow-anything list
workflow-anything validate --workflow wf.yaml
workflow-anything run      --workflow wf.yaml
workflow-anything status   --workflow wf.yaml
workflow-anything visualize --workflow wf.yaml --format mermaid
workflow-anything lint     --workflow wf.yaml
```

## Templates

- `standard` : validate → execute → verify
- `epic_pipeline` : draft → review → implement → validate

## Strate

L3 — orchestration déclarative, zéro GPU.

---

*IntentHash: 0xCTULU_WORKFLOW_ANYTHING_20260612*
*PRD: PRD-034-v1-workflow-anything.md*
*[CONFORME_NEXUS]*
