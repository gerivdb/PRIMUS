# SKILL: container-anything
## Version: 1.0.0 | Score: 16/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [E, Obs]

---

### CAPACITES
- [x] `build` — Build image depuis Dockerfile (--dry-run dispo)
- [x] `run` — Lance container (idempotent — skip si running)
- [x] `stop` — Arrête container (gate HITL)
- [x] `rm` — Supprime container/image (gate HITL obligatoire)
- [x] `inspect` — État détaillé container (Obs pur)
- [x] `ps` — Liste containers actifs
- [x] `compose` — Wrapper docker-compose/podman-compose
- [x] Auto-détection runtime Docker/Podman
- [x] WAL intégration (ARGUS trace)

### ENTREE
```json
{
  "target": "Dockerfile|image:tag|container_id|compose_file",
  "runtime": "docker|podman|null",
  "mode": "build|run|stop|rm|inspect|ps|compose",
  "dry_run": true,
  "wal": true,
  "output": "json|text"
}
```

### SORTIE (ContainerStatus — Contrat A2)
```json
{
  "id": "string",
  "name": "string",
  "image": "string",
  "status": "built|running|stopped|removed|error|not_found|unknown",
  "ports": "string",
  "created": "string",
  "runtime": "docker|podman"
}
```

### GARANTIES
- [OK] `--dry-run` disponibles sur toutes les opérations destructives
- [OK] `--output json` retourne JSON valide parseable
- [OK] rm déclenche un gate HITL si pas en dry-run
- [OK] Idempotent en mode dry
- [OK] WAL entry émise si `--wal`
- [OK] Support Docker ET Podman (runtime auto-détecté)

### FONCTEUR
```
F: E(container_spec) → E(container_running) ∘ Obs(container_status)
```

### DEPENDANCES
- Python 3.10+
- Docker OU Podman installé
- container_schema.py, docker_driver.py, podman_driver.py (même répertoire)

### EXEMPLES
```bash
# Build depuis Dockerfile
python -m container_anything build --target ./Dockerfile --runtime docker

# Run en dry-run
python container.py run --target nginx:latest --mode run --dry-run --output json

# Inspect container
python container.py inspect --target <container_id> --mode inspect --output json

# Liste containers
python container.py ps --target --mode ps --output json

# Supprime (gate HITL si pas dry-run)
python container.py rm --target <container_id> --mode rm --dry-run

# Compose
python container.py compose --target docker-compose.yml --mode compose --dry-run
```

### INTEGRATIONS
```
KIVA pipelines    ← build + run
deploy-anything   ← livraison via container
gate-anything     ← HITL avant stop/rm
scan-anything     ← scan image (secrets, CVE)
ARGUS WAL         ← trace toutes mutations
```

---
*IntentHash: 0xCTULU_CONTAINER_ANYTHING_20260612 | gerivdb/CTULU | Phase 7 | 2026-06-12*
