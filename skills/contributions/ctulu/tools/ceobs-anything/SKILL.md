# SKILL: ceobs-anything
## Version: 0.1.0 | Score: 17/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: Obs

---

### CAPACITES
- [ ] `classify` — Classifie un artefact en C/E/Obs avec score de confiance
- [ ] `classify --emit-yaml` — Génère bloc ternary_role: YAML prêt à patcher
- [ ] `classify --layer` — Boost heuristique par strate (ADR-006)
- [ ] `classify gerivdb/*` — Classification batch sur org entière

### ENTREE
```json
{"target": "string", "layer": "string|null"}
```

### SORTIE
```json
{
  "status": "ok|warn",
  "classification": {
    "primary": "C|E|Obs",
    "confidence": 0.75,
    "hybrid": false,
    "scores": {"C": 0.75, "E": 0.15, "Obs": 0.10}
  },
  "wal_entry": "string|null"
}
```

### GARANTIES
- [OK] `--dry-run` disponible
- [OK] `--json` retourne JSON valide parseable
- [OK] `warn` si confiance < 30%, `ok` sinon
- [OK] Idempotent
- [OK] WAL entry émise si `--wal`

### DEPENDANCES
- Python 3.10+
- PyYAML

### EXEMPLES
```bash
ceobs-anything --target gerivdb/BRAIN --layer L2b_CORRELATOR --output json
ceobs-anything --target tools/fonct-anything/fonct.py --emit-yaml
```

---
*Généré par scaffold-anything --template skill-md | gerivdb/CTULU | [CONFORME_NEXUS]*
