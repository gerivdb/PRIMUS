# keel-anything — SKILL.md

## Description

`keel-anything` is the T1→T5 thought-chain file manager for the CTULU toolset.
It creates, reads, validates, lists, searches, and links `.keel` files — structured
Markdown documents with YAML frontmatter encoding the T1→T5 reasoning chain.

## T-Type Schema

| Type | Name | Required Fields |
|------|------|-----------------|
| T1 | Observation | `timestamp`, `source`, `signal` |
| T2 | Hypothesis | `t1_ref`, `hypothesis`, `confidence` |
| T3 | Decision | `t2_ref`, `decision`, `rationale` |
| T4 | Action | `t3_ref`, `action`, `executor` |
| T5 | Validation | `t4_ref`, `outcome`, `phi_cps_delta` |

Each level references the previous, forming an auditable reasoning chain.

## Usage

```bash
# Create a T1 observation
python tools/keel-anything/keel.py create \
  --target thoughts/obs-001 \
  --t-type T1 \
  --data '{"source":"manual","signal":"anomaly detected"}' \
  --body "Detailed observation notes."

# Read a .keel file
python tools/keel-anything/keel.py read --target thoughts/obs-001.keel

# Validate structure
python tools/keel-anything/keel.py validate --target thoughts/obs-001.keel

# List all .keel files in a directory
python tools/keel-anything/keel.py list --target thoughts/

# Search across .keel files
python tools/keel-anything/keel.py search --target thoughts/ --query "anomaly"

# Link to an ADR
python tools/keel-anything/keel.py link --target thoughts/obs-001.keel --ref ADR-001

# Dry-run create (no file written)
python tools/keel-anything/keel.py create --target thoughts/test --t-type T1 \
  --data '{"source":"test","signal":"test"}' --dry-run

# Text output
python tools/keel-anything/keel.py read --target thoughts/obs-001.keel --output text
```

## File Format

A `.keel` file is Markdown with YAML frontmatter:

```markdown
---
t_type: T1
timestamp: "2026-06-12T06:51:27+00:00"
source: manual
signal: anomaly detected
---

Detailed observation notes.
```

## Modules

| File | Purpose |
|------|---------|
| `keel.py` | CLI entry point (argparse) |
| `keel_crud.py` | CRUD operations (`KeelCRUD` class) |
| `keel_schema.py` | T1→T5 validation (`validate_keel()`) |
| `tool.yaml` | Tool metadata |
| `SKILL.md` | This file |

## Integration

- **ADR cross-references**: Use `link` mode to bind a `.keel` to an ADR/EPIC/intent.
- **WAL trace**: Pass `--wal` to emit a WAL entry to stderr.
- **EPIC-026**: This tool implements EPIC-026.

## IntentHash

`0xCTULU_KEEL_ANYTHING_20260612`
