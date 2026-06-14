# SKILL: cluster-anything
## Version: 1.0.0 | Status: ACTIVE
## Repo: gerivdb/CTULU | IntentHash: 0xCTULU_CLUSTER_ANYTHING_20260612

---

### CAPACITES
- [x] `create` — Crée un nouveau cluster spec (JSON) dans clusters/
- [x] `read` — Lit et affiche un cluster par nom
- [x] `update` — Met à jour version/repos/metadata/edges d'un cluster
- [x] `delete` — Supprime un cluster (gate: confirm requis)
- [x] `list` — Liste tous les clusters
- [x] `validate` — Valide un cluster spec contre CLUSTER_SCHEMA
- [x] `merge` — Fusionne deux clusters, déduplique repos et edges
- [x] `add-repo` — Ajoute un repo (slug + role) à un cluster
- [x] `remove-repo` — Retire un repo d'un cluster

### ENTREE
```json
{
  "target": "string (cluster name or .json path)",
  "mode": "create|read|update|delete|list|validate|merge|add-repo|remove-repo",
  "dry_run": "bool",
  "wal": "bool",
  "output": "json|text|mermaid"
}
```

### SORTIE
```json
{
  "status": "ok|error",
  "errors": ["string"],
  "cluster": {"name": "", "version": "", "repos": [], "metadata": {}, "edges": []},
  "wal_entry": "string|null"
}
```

### FORMAT CLUSTER SPEC
```json
{
  "name": "my-cluster",
  "version": "1.0.0",
  "repos": [
    {"slug": "gerivdb/REPO", "role": "primary", "metadata": {}}
  ],
  "metadata": {"created_at": "", "updated_at": ""},
  "edges": [
    {"from": "slug-a", "to": "slug-b", "type": "depends", "weight": 1.0}
  ]
}
```

### GARANTIES
- [OK] `--dry-run` disponible — aucun fichier écrit
- [OK] `--wal` émet une WAL entry horodatée
- [OK] `--output json|text|mermaid` — 3 formats de sortie
- [OK] `delete` et `merge` requièrent un gate (confirm / second-cluster)
- [OK] Validation schema sur create/update/merge
- [OK] Dédoublonnage des repos par slug et des edges par (from, to)

### DEPENDANCIES
- Python 3.10+
- Aucune dépendance externe (stdlib uniquement)

### EXEMPLES
```bash
python cluster.py --mode create --target my-cluster --version 1.0.0 --repos '[{"slug":"gerivdb/BRAIN","role":"primary"}]'
python cluster.py --mode read --target my-cluster --output json
python cluster.py --mode list --output text
python cluster.py --mode validate --target my-cluster
python cluster.py --mode add-repo --target my-cluster --repo-slug gerivdb/ONTOLOGY --role secondary
python cluster.py --mode remove-repo --target my-cluster --repo-slug gerivdb/ONTOLOGY --dry-run
python cluster.py --mode merge --target cluster-a --second-cluster cluster-b
python cluster.py --mode delete --target my-cluster --confirm
```

### PIPELINE TYPIQUE
```bash
# Créer un cluster pour un EPIC
python cluster.py --mode create --target epic-027-cluster \
  --repos '[{"slug":"gerivdb/CTULU","role":"primary"},{"slug":"gerivdb/BRAIN","role":"secondary"}]' \
  --output json --wal

# Valider avant merge
python cluster.py --mode validate --target epic-027-cluster

# Fusionner deux clusters
python cluster.py --mode merge --target cluster-a --second-cluster cluster-b --output mermaid
```

---
*EPIC-027 | gerivdb/CTULU | cluster-anything v1.0.0*
