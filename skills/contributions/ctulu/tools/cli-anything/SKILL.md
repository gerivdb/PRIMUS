# SKILL: cli-anything
## Version: 0.1.0-wrapper | Score: 17/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [E, C]

---

### CAPACITES
- [ ] `generate` — Génère SKILL.md + HARNESS.md + cli.py pour un repo
- [ ] `validate` — Valide SKILL.md existant (délègue à audit-anything)
- [ ] `discover` — Découvre les skills dans un répertoire ou org
- [ ] `score` — Calcule le score SKILL (0-20) d'un repo

### ENTREE
```json
{"target": "string", "skill_name": "string|null", "output_dir": "string"}
```

### SORTIE
```json
{
  "status": "ok|error",
  "target": "string",
  "changes": [{"file": "", "action": "created|dry-run"}],
  "wal_entry": "string|null"
}
```

### GARANTIES
- [OK] `--dry-run` disponible — aucun fichier écrit
- [OK] `--json` retourne JSON valide parseable
- [OK] Utilise les templates scaffold-anything (skill-md, harness-md, cli-click)
- [OK] Idempotent — double génération = même résultat
- [OK] WAL entry émise si `--wal`

### DEPENDANCES
- Python 3.10+
- scaffold-anything templates
- audit-anything (pour validate)

### EXEMPLES
```bash
cli-anything generate --target gerivdb/CANDIDATOR --output-dir ./out
cli-anything generate --target gerivdb/NEXUS --dry-run --output json
cli-anything validate --target ./SKILL.md
cli-anything discover --target gerivdb/ --output json
```

### PIPELINE EPIC-222
```bash
ceobs-anything --target <repo> --emit-yaml \
  | cli-anything generate --target <repo> \
  | audit-anything --rule skill-md-format \
  | gate-anything --mode hitl \
  | migrate-anything --target NEXUS-registry
```

---
*Généré par scaffold-anything --template skill-md | gerivdb/CTULU | [CONFORME_NEXUS]*
