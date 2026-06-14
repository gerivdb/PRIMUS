# skill-anything — Universal Skill Factory

## Description

`skill-anything` is the meta-skill factory for CTULU tools. It creates, validates, scores, lists, diffs, generates, and tests skill files with valid YAML frontmatter and mandatory sections.

## Usage

```bash
python skill.py --mode create --target my-skill --dry-run
python skill.py --mode validate --target my-skill/SKILL.md
python skill.py --mode score --target my-skill/SKILL.md --output json
python skill.py --mode list --target tools/
python skill.py --mode diff --target a/SKILL.md --target-b b/SKILL.md
python skill.py --mode generate --target my-skill
python skill.py --mode test --target my-skill/SKILL.md
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--target` | str | None | Skill file path or skill name |
| `--target-b` | str | None | Second target for diff mode |
| `--mode` | str | None | create\|validate\|score\|list\|diff\|generate\|test |
| `--dry-run` | bool | False | Simulation only, no file written |
| `--wal` | bool | False | Enable write-ahead log |
| `--output` | str | text | Output format: json\|text |

## Scoring Criteria (0-20)

| Criterion | Points | Condition |
|-----------|--------|-----------|
| Frontmatter completeness | 3 | All 6 fields present and valid |
| Mandatory sections | 5 | Description, Usage, Parameters, Examples, Output, Contract |
| Examples | 3 | Code blocks present in Examples section |
| Contracts | 3 | Parseable YAML contract block |
| Tests | 3 | tests/ directory exists |
| Documentation | 3 | Description >100 chars, Parameters table, Output section |

## Examples

### Create a new skill

```bash
python skill.py --mode create --target audit-anything
```

### Validate existing skill

```bash
python skill.py --mode validate --target tools/skill-anything/SKILL.md
```

### Score a skill (JSON output)

```bash
python skill.py --mode score --target tools/skill-anything/SKILL.md --output json
```

## Output

- **create**: `{action, path, dry_run, valid}`
- **validate**: `{valid, path, checks}`
- **score**: `{score, max: 20, path}`
- **list**: `{skills: [...], count}`
- **diff**: `{target_a, target_b, changes: [...], has_changes, valid}`
- **generate**: Same as create with `dry_run: true`
- **test**: `{target, pass, checks: [...], errors: [...], checks_passed, checks_total}`

## Contract

```yaml
args: [--target, --target-b, --mode, --dry-run, --wal, --output]
output: {score: int, valid: bool, skills: list}
```

---
*IntentHash: 0xCTULU_SKILL_ANYTHING_20260612*
