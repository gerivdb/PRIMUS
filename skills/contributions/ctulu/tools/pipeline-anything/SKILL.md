# pipeline-anything — SKILL.md

## Description

`pipeline-anything` is the declarative data pipeline runner for the CTULU toolset.
It creates, runs, monitors, visualizes, and replays data pipelines defined as
YAML specs. Every operation is traceable via WAL and supports dry-run mode.

## Foncteur

```
F: (E(run) ∘ C(spec)) → Obs(status_stream)
```

## Ternary Role

- **Primary**: E (execution), C (creation)
- **Secondary**: Obs (monitoring)

## Usage

```bash
# Create a pipeline spec skeleton
python tools/pipeline-anything/pipeline.py create \
  --target specs/my-pipeline.yaml \
  --name my-pipeline \
  --inputs "raw_data.csv" \
  --outputs "clean_data.parquet" \
  --mode create --dry-run

# Validate a spec
python tools/pipeline-anything/pipeline.py \
  --target specs/my-pipeline.yaml \
  --mode validate \
  --output json

# Run a pipeline
python tools/pipeline-anything/pipeline.py \
  --target specs/my-pipeline.yaml \
  --mode run --wal

# Dry-run (zero side effects)
python tools/pipeline-anything/pipeline.py \
  --target specs/my-pipeline.yaml \
  --mode run --dry-run

# Check status
python tools/pipeline-anything/pipeline.py \
  --target specs/my-pipeline.yaml \
  --mode status

# Visualize as Mermaid
python tools/pipeline-anything/pipeline.py \
  --target specs/my-pipeline.yaml \
  --mode visualize

# Diff two specs
python tools/pipeline-anything/pipeline.py \
  --target specs/v1.yaml \
  --mode diff \
  --compare specs/v2.yaml

# Replay
python tools/pipeline-anything/pipeline.py \
  --target specs/my-pipeline.yaml \
  --mode replay --wal

# Abort (requires gate confirmation: type 'ABORT')
python tools/pipeline-anything/pipeline.py \
  --target specs/my-pipeline.yaml \
  --mode abort
```

## Spec Format

```yaml
name: my-pipeline
version: "1.0.0"
steps:
  - name: extract
    command: "python extract.py --input raw.csv"
    depends_on: []
    inputs: [raw.csv]
    outputs: [extracted.parquet]
  - name: transform
    command: "python transform.py --input extracted.parquet"
    depends_on: [extract]
    inputs: [extracted.parquet]
    outputs: [transformed.parquet]
  - name: load
    command: "python load.py --input transformed.parquet"
    depends_on: [transform]
    inputs: [transformed.parquet]
    outputs: [final.db]
inputs:
  - raw.csv
outputs:
  - final.db
metadata:
  author: gerivdb
  created: "2026-06-12"
```

## Modules

| File | Purpose |
|------|---------|
| `pipeline.py` | CLI entry point (argparse, 8 sub-commands) |
| `pipeline_spec.py` | Spec model (`PipelineSpec`, `PipelineStep`) |
| `pipeline_runner.py` | Execution engine (`PipelineRunner`, `PipelineResult`) |
| `pipeline_visualizer.py` | Mermaid flow generation (`render_mermaid`) |
| `tool.yaml` | Tool metadata |
| `SKILL.md` | This file |

## Abort Gate

`--mode abort` requires explicit user confirmation:

```
CONFIRM ABORT: Type 'ABORT' to confirm cancellation of '<name>': 
```

Abort is blocked unless the user types exactly `ABORT`. The gate is
bypassed only in `--dry-run` mode (prints simulation).

## WAL

Pass `--wal` to write JSONL entries to `wal/<name>_WAL.jsonl`.
Each entry contains: `timestamp`, `pipeline`, `action`, `status`, `details`.

## Dependencies

- Python 3.10+
- PyYAML

## EPIC

EPIC-033 | IntentHash: `0xCTULU_EPIC033_PIPELINE_ANYTHING_20260612`
