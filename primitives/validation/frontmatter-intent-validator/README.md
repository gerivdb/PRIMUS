---
type: primitive
version: "1.0.0"
date: "2026-08-19"
intent_hash: 0xPRIMITIVE_FRONTMATTER_INTENT_VALIDATOR_20260819
status: active
category: validation
---

# Primitive: frontmatter_intent_validator

## Responsibility
Validate INTENT frontmatter and required sections.

## Contract
- Input: `file_path: str` (path to INTENT-*.md)
- Output: `ValidationResult` {valid, errors, error_count}
- Side effects: none
- Dependencies: stdlib only

## Usage
```python
from frontmatter_intent_validator import frontmatter_intent_validator

result = frontmatter_intent_validator("INTENTS/INTENT-MCP-SYNAPTIC-ECOSYSTEM-VISION-2026-08-19.md")
if result.valid:
    print("VALID")
else:
    for err in result.errors:
        print(f"INVALID: {err.message}")
```

## Verification
```bash
python -m frontmatter_intent_validator INTENTS/INTENT-MCP-SYNAPTIC-ECOSYSTEM-VISION-2026-08-19.md
```

## Ref
- PRIMUS/primitives/validation/json_schema_validator.py (sibling primitive)
