---
type: primitive
version: "1.0.0"
date: "2026-08-19"
intent_hash: 0xPRIMITIVE_INTENT_HASH_GEN_20260819
status: active
category: validation
---

# Primitive: intent_hash_gen

## Responsibility
Generate a valid IntentHash from a human slug, with collision detection against existing INTENTS/.

## Contract
- Input: `slug: str` (ex: "INTENT-MCP-SYNAPTIC-ECOSYSTEM-VISION-20260819_v10")
- Output: `intent_hash: str` (format `0xSLUG_MAJUSCULES`)
- Side effects: none
- Dependencies: stdlib only

## Usage
```python
from intent_hash_gen import generate_intent_hash, slug_to_intent_hash

# Generate with collision check
ih = generate_intent_hash("INTENT-MCP-SYNAPTIC-ECOSYSTEM-VISION-20260819_v10", "INTENTS")
# -> 0xINTENT_MCP_SYNAPTIC_ECOSYSTEM_VISION_20260819_V10

# Just convert without check
ih = slug_to_intent_hash("INTENT-MCP-SYNAPTIC-ECOSYSTEM-VISION-20260819_v10")
# -> 0xINTENT_MCP_SYNAPTIC_ECOSYSTEM_VISION_20260819_V10
```

## Verification
```bash
python -m intent_hash_gen "INTENT-MCP-SYNAPTIC-ECOSYSTEM-VISION-20260819_v10"
```

## Ref
- PRIMUS/primitives/validation/json_schema_validator.py (sibling primitive)
