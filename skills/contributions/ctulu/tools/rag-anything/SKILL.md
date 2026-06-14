---
name: rag-anything
version: "1.0.0"
description: |
  RAG Anything — Outil universel de Retrieval-Augmented Generation pour l'écosystème CTULU.
  Indexe, interroge, valide et exporte des chunks de connaissance depuis n'importe quelle source.
allowed-tools: [read, write, edit, bash]
metadata: {lang: python, target: D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\tools\rag-anything}
---

# SKILL.md — rag-anything

## Description

RAG Anything est un outil CLI en Python qui implémente un pipeline RAG complet :
indexation, interrogation par mots-clés (scoring TF simplifié), validation de fraîcheur,
diff, export LLM-ready et injection de contexte.

## Architecture

```
tools/rag-anything/
├── rag.py            # CLI argparse (point d'entrée)
├── rag_index.py      # RagIndexer — indexation chunks/fichiers/répertoires
├── rag_query.py      # RagQuery — moteur de recherche TF
├── rag_validate.py   # Validation fraîcheur (>30j = obsolète)
├── rag_export.py     # Export LLM-ready (markdown / JSON)
├── tool.yaml         # Métadonnées outil
└── SKILL.md          # Ce fichier
```

## Utilisation

### Indexer un fichier
```bash
python -m rag_anything --mode index --target ./mon_fichier.md --output text
```

### Indexer un répertoire
```bash
python -m rag_anything --mode index --target ./docs/ --glob "*.md" --save index.json
```

### Interroger
```bash
python -m rag_anything --mode query --target ./docs/ --query "architecture ADR" --output text
```

### Valider la fraîcheur
```bash
python -m rag_anything --mode validate --save index.json --output text
```

### Exporter pour LLM
```bash
python -m rag_anything --mode export --query "sujet" --save index.json --fmt markdown
```

### Prune (avec gate)
```bash
python -m rag-anything --mode prune --save index.json --gate CONFIRM_PRUNE
python -m rag_anything --mode prune --save index.json --gate CONFIRM_PRUNE --dry-run
```

### Diff
```bash
python -m rag_anything --mode diff --target ./docs/ --save index.json
```

### Inject (contexte XML pour LLM)
```bash
python -m rag_anything --mode inject --query "recherche" --top-k 3 --output text
```

### Mode inline (indexer une chaîne)
```bash
python -m rag_anything --mode index --target rag:inline --content "Contenu à indexer" --output text
```

## Paramètres communs

| Paramètre | Description |
|-----------|-------------|
| `--target` | rag_context (AGENT_RAM, SKILLS, BRAIN, WAL) ou chemin fichier/répertoire |
| `--mode` | index, query, update, diff, validate, prune, export, inject |
| `--query` | Chaîne de recherche (query, export, inject) |
| `--dry-run` | Simulation sans effet de bord |
| `--wal` | Active l'entrée WAL |
| `--output` | json (défaut) ou text |
| `--save` | Chemin persistance JSON de l'index |

## Format de sortie JSON

```json
{
  "status": "ok",
  "target": "./docs/",
  "data": { ... },
  "tool": "rag-anything",
  "timestamp": "2026-06-12T...",
  "wal_entry": null
}
```

## Chunk Schema

```python
{
  "id": "sha256[:16]",
  "source": "chemin/fichier",
  "content": "texte du chunk",
  "embedding": [float × 16],  # simulé via SHA-256
  "metadata": {...},
  "indexed_at": "ISO-8601 UTC"
}
```

## Scoring

Le scoring est basé sur TF (Term Frequency) simplifié :
- Chaque token de la requête est pondéré par sa fréquence dans le chunk
- Score = somme(TF token) / (TF max × nb tokens requête)
- Seuls les chunks avec score > 0 sont retournés

## Validation

La validation détecte :
- Chunks sans `indexed_at` ou timestamp invalide
- Chunks de plus de 30 jours (seuil `FRESHNESS_DAYS`)
- Contenu vide ou suspectement court (< 10 chars)
- Embedding invalide (longueur != 16)

## Prune Gate

Le `prune` nécessite `--gate CONFIRM_PRUNE`. Sans ce gate exact,
la commande retourne une erreur. Le `--dry-run` permet de simuler.

## Cibles RAG spéciales

| Target | Description |
|--------|-------------|
| AGENT_RAM | Mémoire agentique (contexte runtime) |
| SKILLS | Skills KiloCode CTULU |
| BRAIN | Dépôt BRAIN |
| WAL | Write-Ahead Log entries |
| chemin fichier | Tout fichier texte |
| chemin répertoire | Récursif avec glob pattern |

## Dépendances

- Python 3.10+
- Aucune dépendance externe (stdlib uniquement)
