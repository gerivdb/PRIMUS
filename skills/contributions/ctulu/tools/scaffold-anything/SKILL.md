# SKILL: scaffold-anything
## Version: 0.1.0 | Score: 16/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: E

---

### CAPACITES
- [ ] `scaffold` — Génère un composant CEObs-conforme depuis un template
- [ ] `scaffold --template skill-md` — Génère SKILL.md (standard CLI-Anything)
- [ ] `scaffold --template harness-md` — Génère HARNESS.md
- [ ] `scaffold --template cli-click` — Génère cli.py Click + --json
- [ ] `scaffold --template tool-yaml` — Génère tool.yaml CEObs-conforme
- [ ] `scaffold --template prd` — Génère PRD RSS-v1

### ENTREE
```json
{"target": "string", "template": "string", "variables": {}}
```

### SORTIE
```json
{
  "status": "ok|warn|error",
  "target": "string",
  "files_generated": ["string"],
  "wal_entry": "string|null"
}
```

### GARANTIES
- [OK] `--dry-run` disponible — affiche rendu sans écrire
- [OK] `--json` retourne JSON valide parseable
- [OK] Tout template est versionné dans templates/
- [OK] Idempotent — double scaffold = même résultat
- [OK] WAL entry émise si `--wal`

### DEPENDANCES
- Python 3.10+
- PyYAML

### EXEMPLES
```bash
scaffold-anything --template skill-md --target gerivdb/CANDIDATOR --output-dir ./out
scaffold-anything --template cli-click --target my-tool --dry-run --output json
```

---
*Généré par scaffold-anything --template skill-md | gerivdb/CTULU | [CONFORME_NEXUS]*
