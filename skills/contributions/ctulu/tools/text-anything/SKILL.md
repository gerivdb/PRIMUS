# SKILL: text-anything
## Version: 1.0.0 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: C (E, Obs)

---

### CAPACITES
- [x] `extract` — Extrait des patterns (MADR, intent-hashes, keel, changelog, foncteurs)
- [x] `transform` — Transforme (md→json, yaml→md)
- [x] `generate` — Génère texte depuis template + data
- [x] `validate` — Valide la structure d'un document
- [x] `diff` — Diff sémantique entre deux textes
- [x] `normalize` — Normalise encodage, fin de lignes, espaces

### ENTREE
```bash
text-anything extract --pattern madr --target file.md --output json
text-anything transform --mode md-to-json --target file.md
text-anything generate --template madr --data '{"title":"X"}'
text-anything validate --pattern madr --target file.md
text-anything diff --target a.md --target-b b.md --semantic
text-anything normalize --target file.md
```

### SORTIE
```json
{
  "status": "ok|error",
  "result": {},
  "wal_entry": "path|null"
}
```

### GARANTIES
- [OK] `--output json` retourne JSON valide parseable
- [OK] `--output text` retourne texte brut
- [OK] `--output md` retourne Markdown structuré
- [OK] `--wal` écrit entrée WAL pour traçabilité
- [OK] `--target stdin` depuis pipe
- [OK] `--target <fichier>` lit fichier unique
- [OK] `--target <répertoire>` scanne récursivement les .md
- [OK] Mode `diff --semantic` compare headings/links/pas le raw
- [OK] Mode `normalize` supprime trailing whitespace + fin de lignes mixtes

### DEPENDANCES
- Python 3.10+
- PyYAML

### EXEMPLES
```bash
# Extraire un MADR depuis un fichier
python -m text_anything extract --pattern madr --target ADR.md --output json

# Extraire tous les intent hashes
python -m text_anything extract --pattern intent-hash --target file.md

# Transformer Markdown → JSON
python -m text_anything transform --mode md-to-json --target doc.md

# Générer un ADR depuis template
python -m text_anything generate --template madr --data '{"title":"X","contexte":"Y","decision":"Z"}'

# Valider la structure MADR
python -m text_anything validate --pattern madr --target ADR.md

# Diff sémantique
python -m text_anything diff --target a.md --target-b b.md --semantic

# Normaliser
python -m text_anything normalize --target file.md --in-place
```

### FONCTEUR
```
F: C(text) → C(structured_data) ∘ E(pattern_match) ∘ Obs(validation_report)
```

Text-Anything est C primaire : il ne modifie jamais les artefacts source
(sauf --in-place pour normalize). Il extrait, transforme, valide.

### TEMPLATES DISPONIBLES
| ID | Usage |
|---|---|
| `madr` | Génère un ADR au format MADR |
| `changelog-entry` | Génère une entrée de changelog |
| `keel-signal` | Génère un signal Keel |
| `intent-declaration` | Déclare un intent hash |
| `foncteur-doc` | Documente un foncteur |

### PATTERNS D'EXTRACTION
| Pattern | Extrait |
|---|---|
| `madr` | status, date, title, contexte, décision, conséquences, risques, options |
| `intent-hash` | Tous les tokens 0x... |
| `keel` | T-type, timestamp, T1→T5 |
| `changelog` | version, date, added/changed/fixed |
| `foncteur` | Toutes les déclarations F_* |

---
*IntentHash: 0xCTULU_TEXT_ANYTHING_20260612 | gerivdb/CTULU | Phase 7 | 2026-06-12*
