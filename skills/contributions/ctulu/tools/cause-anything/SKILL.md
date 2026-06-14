# SKILL.md — cause-anything
# Version: 1.0.0 | Status: ACTIVE
# Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [C, Obs]

## CAPACITES
- [x] `build` — Construit un DAG causal à partir de données ou matrice de corrélation
- [x] `validate` — Valide un DAG (acyclic, connected)
- [x] `export` — Exporte vers WAL ARGUS

## ENTREE
{"target": "<correlation_matrix|data_file>", "mode": "build|validate|export", "method": "pc|granger|lingam|hybrid"}

## SORTIE
{"status": "ok|error", "dag": "CausalDAG|null", "validation": "ValidationResult|null"}

## GARANTIES
- [OK] DAG produit est acyclique
- [OK] Export WAL ARGUS traçable
- [OK] Validation détection de cycles

## DEPENDANCES
- Python 3.10+
- WAL ARGUS (externe)

## EXEMPLES
```bash
# Construire un DAG causal
cause-anything build --target correlation.json --method pc

# Valider un DAG
cause-anything validate --target dag.json

# Exporter vers ARGUS
cause-anything export --target dag.json --wal
```

---
*IntentHash: 0xCTULU_CAUSE_ANYTHING_20260613*
*Généré pour EPIC-096 | gerivdb/CTULU | [CONFORME_NEXUS]*
