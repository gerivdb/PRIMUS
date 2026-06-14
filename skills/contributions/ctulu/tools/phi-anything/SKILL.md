# SKILL: phi-anything
## Version: 1.0.0 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L4_TOOLS | ternary_role: [Obs, C]

---

### CAPACITES
- [x] `get` — Retourne le phi_cps courant pour une cible
- [x] `diff` — Compare phi_cps entre deux instants (WAL)
- [x] `history` — Historique phi_cps depuis WAL ARGUS
- [x] `watch` — Mode continu, alerte si phi_cps < floor
- [x] `threshold` — Vérifie si phi_cps >= seuil (CI-friendly, exit code)
- [x] `events` — Liste PHI_DEGRADATION / PHI_TRANSCENDANCE

### ENTREE
```json
{"target": "string", "mode": "get|diff|history|watch|threshold|events", "output": "json|text|chart"}
```

### SORTIE
```json
{
  "status": "ok|below_threshold|error",
  "action": "get|diff|history|watch|threshold|events",
  "target": "string",
  "report": "PhiReport|null",
  "diff": "DiffResult|null",
  "history": "list[PhiEntry]|null",
  "events": "list[PhiEvent]|null",
  "alerts": "list[PhiAlert]|null",
  "wal_entry": "string|null"
}
```

### GARANTIES
- [OK] `--output json|text|chart` supporté partout
- [OK] Validation schema PhiReport (target, phi_cps, delta, timestamp, status, events)
- [OK] WAL entry émise si `--wal`
- [OK] `threshold` exit code 0 si >= seuil, 1 sinon (CI-friendly)
- [OK] `watch` mode continu avec intervalle configurable
- [OK] Mock fallback si phi_ecosystem.json absent
- [OK] `--event-type` filtre PHI_DEGRADATION / PHI_TRANSCENDANCE

### SEUILS PHI
| Valeur phi_cps | Status | Événement |
|---|---|---|
| >= 4.559 | transcended | PHI_TRANSCENDANCE |
| 4.0 – 4.559 | ok | — |
| < 4.0 | degraded | PHI_DEGRADATION |

### DEPENDANCES
- Python 3.10+
- Aucune dépendance externe (stdlib uniquement)

### EXEMPLES
```bash
# Lire le phi_cps courant
phi-anything get --target ecosystem

# Diff entre maintenant et un timestamp
phi-anything diff --target repo:CTULU --compare 2026-06-11T00:00:00Z

# Historique des 20 dernières entrées
phi-anything history --target all --limit 20

# Watch mode : alerte si phi_cps < 4.559
phi-anything watch --target ecosystem --floor 4.559 --interval 30

# CI gate : exit 1 si phi_cps < 4.559
phi-anything threshold --target ecosystem --threshold 4.559

# Lister les événements de dégradation
phi-anything events --target ecosystem --event-type PHI_DEGRADATION

# Sortie JSON + WAL
phi-anything get --target ecosystem --output json --wal

# Chart visuel
phi-anything get --target ecosystem --output chart
```

---
*IntentHash: 0xCTULU_PHI_ANYTHING_20260612*
*Généré pour EPIC-028 | gerivdb/CTULU | [CONFORME_NEXUS]*
