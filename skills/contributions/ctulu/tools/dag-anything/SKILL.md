# SKILL: dag-anything
## Version: 1.0.0 | Status: ACTIVE
## Repo: gerivdb/CTULU | IntentHash: 0xCTULU_DAG_ANYTHING_20260612

---

### CAPACITES
- [x] `build` — Construit un DAG depuis un spec YAML ou un graphe de dépendances
- [x] `query` — Requêtes : dependencies, dependents, roots, leaves
- [x] `validate` — Détecte cycles, orphans, étoiles mortes
- [x] `visualize` — Rendu Mermaid flowchart ou Graphviz DOT
- [x] `diff` — Compare deux DAGs (added/removed nodes et edges)
- [x] `topo-sort` — Tri topologique (Kahn's algorithm)
- [x] `critical-path` — Chemin critique (longue chaîne de dépendances)
- [x] `export` — Exporte en JSON, Mermaid, DOT, GraphML

### ENTREE
```json
{
  "target": "string (dag_spec YAML file, repo path, or dependency graph JSON)",
  "mode": "build|query|validate|visualize|diff|topo-sort|critical-path|export",
  "dry_run": "bool",
  "wal": "bool",
  "output": "json|mermaid|dot|graphml"
}
```

### SORTIE
```json
{
  "status": "ok|error",
  "errors": ["string"],
  "dag": {"nodes": [], "edges": [], "metadata": {}},
  "result": {},
  "wal_entry": "string|null"
}
```

### FORMAT DAG SPEC (YAML)
```yaml
name: my-dag
version: "1.0.0"
nodes:
  - id: A
    label: "Task A"
    weight: 1
  - id: B
    label: "Task B"
    weight: 2
edges:
  - from: A
    to: B
    weight: 1
metadata:
  created: "2026-06-12"
```

### FORMAT DEP GRAPH (JSON)
```json
{
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["D"],
  "D": []
}
```

### GARANTIES
- [OK] `--dry-run` disponible — aucun fichier écrit
- [OK] `--wal` émet une WAL entry horodatée
- [OK] `--output json|mermaid|dot|graphml` — 4 formats de sortie
- [OK] Validation DFS-based cycle detection
- [OK] Tri topologique via Kahn's algorithm
- [OK] Détection orphans (nodes sans edges) et dead-end stars

### DEPENDANCIES
- Python 3.10+
- PyYAML (pour build_from_spec YAML files)
- Aucune autre dépendance externe (stdlib uniquement)

### EXEMPLES
```bash
python dag.py --mode build --target dag_spec.yaml --output json
python dag.py --mode build --target '{"A":["B"],"B":["C"],"C":[]}' --output json
python dag.py --mode validate --target dag_spec.yaml
python dag.py --mode query --target dag_spec.yaml --query-type dependencies --node A
python dag.py --mode visualize --target dag_spec.yaml --output mermaid
python dag.py --mode topo-sort --target dag_spec.yaml
python dag.py --mode critical-path --target dag_spec.yaml
python dag.py --mode diff --target dag_spec.yaml --second-target dag_spec_v2.yaml
python dag.py --mode export --target dag_spec.yaml --output graphml
```

### PIPELINE TYPIQUE
```bash
python dag.py --mode build --target deps.yaml --output json
python dag.py --mode validate --target deps.yaml
python dag.py --mode visualize --target deps.yaml --output mermaid
python dag.py --mode topo-sort --target deps.yaml
python dag.py --mode critical-path --target deps.yaml
```

---
*EPIC-032 | gerivdb/CTULU | dag-anything v1.0.0*
