# SKILL: sabre-anything
## Version: 1.0.0 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L4_TOOLS | ternary_role: [C, E, Obs]

---

### CAPACITES
- [x] `plan` — Calcule la topologie sans l'appliquer
- [x] `apply` — Applique la topologie avec gate de validation
- [x] `diff` — Compare deux topologies (added/removed nodes & edges)
- [x] `render` — Produit Mermaid, DOT ou JSON
- [x] `validate` — Valide les contraintes NEXUS sur la spec

### ENTREE
```json
{"target": "string", "mode": "plan|apply|diff|render|validate", "output": "json|mermaid|dot"}
```

### SORTIE
```json
{
  "status": "ok|dry_run_ok|error|rejected_by_validation|invalid",
  "action": "plan|apply|diff|render|validate",
  "target": "string",
  "graph": "TopologyGraph|null",
  "diff": "DiffResult|null",
  "violations": "list[str]",
  "wal_entry": "string|null"
}
```

### GARANTIES
- [OK] `--dry-run` disponible — aucun effet de bord
- [OK] `--output json|mermaid|dot` supporté partout
- [OK] Validation schema JSON (nodes, edges, metadata)
- [OK] Contraintes NEXUS (self-loops, types inconnus)
- [OK] WAL entry émise si `--wal`
- [OK] `--compare` pour diff deux specs

### DEPENDANCES
- Python 3.10+
- pyyaml
- jsonschema

### EXEMPLES
```bash
# Planifier une topologie
sabre-anything plan --target topology_spec.yaml

# Appliquer en dry-run
sabre-anything apply --target spec.yaml --dry-run

# Diff entre deux specs
sabre-anything diff --target new.yaml --compare old.yaml

# Rendu Mermaid
sabre-anything render --target spec.yaml --output mermaid

# Validation NEXUS
sabre-anything validate --target spec.yaml

# Sortie JSON + WAL
sabre-anything apply --target spec.yaml --wal --output json
```

---
*IntentHash: 0xCTULU_SABRE_ANYTHING_20260612*
*Généré pour EPIC-022 | gerivdb/CTULU | [CONFORME_NEXUS]*
