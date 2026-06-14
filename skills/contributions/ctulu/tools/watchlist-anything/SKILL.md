# SKILL — watchlist-anything

## Description
Manage and trigger watchlists for the CTULU ecosystem. Supports CRUD operations,
schema validation (IRIS), forced signal evaluation, and multi-format output.

## Tool Path
`tools/watchlist-anything/`

## Files
| File | Role |
|------|------|
| `watchlist.py` | CLI entry point (argparse) |
| `watchlist_crud.py` | CRUD operations (WatchlistCRUD class) |
| `watchlist_schema.py` | IRIS JSON Schema validation |
| `watchlist_trigger.py` | Signal evaluation engine |
| `tool.yaml` | Tool metadata |
| `SKILL.md` | This file |

## CLI Usage

```bash
# Create a watchlist
python tools/watchlist-anything/watchlist.py --mode create --target my-watchlist

# Read
python tools/watchlist-anything/watchlist.py --mode read --target my-watchlist

# Update a field
python tools/watchlist-anything/watchlist.py --mode update --target my-watchlist --key threshold --value 5.0

# Delete (requires --gate)
python tools/watchlist-anything/watchlist.py --mode delete --target my-watchlist --gate

# List all
python tools/watchlist-anything/watchlist.py --mode list --target _

# Validate
python tools/watchlist-anything/watchlist.py --mode validate --target my-watchlist

# Trigger evaluation
python tools/watchlist-anything/watchlist.py --mode trigger --target my-watchlist [--dry-run]

# Status (dry-run trigger)
python tools/watchlist-anything/watchlist.py --mode status --target my-watchlist

# Output formats
python tools/watchlist-anything/watchlist.py --mode list --target _ --output json
python tools/watchlist-anything/watchlist.py --mode list --target _ --output yaml
```

## Watchlist YAML Format

```yaml
name: my-watchlist
targets:
  - repo-a
  - repo-b
signals:
  - type: branch_created
    threshold: 1.0
    operator: gte
threshold: 1.0
routes_to:
  - KRONOS
  - OBSERVER
silenced_until: null
created: "2026-06-12T07:00:00+00:00"
last_updated: "2026-06-12T07:00:00+00:00"
```

## Signal Types
`branch_created`, `branch_deleted`, `branch_merged`, `pr_opened`, `pr_closed`,
`pr_merged`, `commit_pushed`, `tag_created`, `release_published`, `file_changed`,
`threshold_breach`, `custom`

## Operators
`gt`, `gte`, `lt`, `lte`, `eq`, `ne`

## Store
Watchlists are stored as YAML files in `tools/watchlist-anything/store/`.

## IntentHash
`0xCTULU_WATCHLIST_ANYTHING_20260612`
