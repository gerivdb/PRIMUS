# verse-anything — Verses de l'écosystème

## Description

Crée, valide, scaffold, diff et merge des Verses (ensembles cohérents
d'artefacts, tools, ou concepts) dans l'écosystème gerivdb.

## Usage

```bash
verse-anything create   --name my-verse --template standard
verse-anything list
verse-anything validate --verse verse.yaml
verse-anything scaffold --verse verse.yaml --output ./verse/
verse-anything diff     --verse-a va.yaml --verse-b vb.yaml
verse-anything merge    --verse-a va.yaml --verse-b vb.yaml
```

## Templates

- `standard` : manifest + axioms + README
- `minimal` : manifest uniquement

## Strate

L3 — scaffolding déclaratif, zéro GPU.

---

*IntentHash: 0xCTULU_VERSE_ANYTHING_20260612*
*PRD: PRD-036-v1-verse-anything.md*
*[CONFORME_NEXUS]*
