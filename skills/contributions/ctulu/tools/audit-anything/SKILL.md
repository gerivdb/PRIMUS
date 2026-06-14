# SKILL: audit-anything
## Version: 0.1.0 | Score: 17/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: C

---

### CAPACITES
- [ ] `audit` — Valide un artefact contre une règle ou un schéma
- [ ] `audit --rule ceobs-missing` — Détecte absence ternary_role.primary (ADR-006)
- [ ] `audit --rule ceobs-schema` — Valide valeurs C/E/Obs
- [ ] `audit --rule rss-v1-compliance` — Vérifie conformité RSS-v1
- [ ] `audit --rule skill-md-format` — Valide structure SKILL.md (PRD-008)
- [ ] `audit --rule harness-md-format` — Valide structure HARNESS.md

### ENTREE
```json
{"target": "string", "rule": "string"}
```

### SORTIE
```json
{
  "status": "ok|warn|error",
  "target": "string",
  "violations": [{"rule": "", "path": "", "detail": ""}],
  "wal_entry": "string|null",
  "phi_cps_delta": 0.0
}
```

### GARANTIES
- [OK] `--dry-run` disponible — aucun effet de bord
- [OK] `--json` retourne JSON valide parseable
- [OK] Exit code `0` si ok, `1` si violations
- [OK] Idempotent — double exécution = même résultat
- [OK] WAL entry émise si `--wal`

### DEPENDANCES
- Python 3.10+
- PyYAML

### EXEMPLES
```bash
audit-anything --target SKILL.md --rule skill-md-format --output json
audit-anything --target gerivdb/ARGUS --rule ceobs-missing --wal
```

---
*Généré par scaffold-anything --template skill-md | gerivdb/CTULU | [CONFORME_NEXUS]*
