# explain-anything — Justification causale LLM-readable

## Description

Export du DAG causal → Markdown narratif HITL-readable.
Génère une justification causale compréhensible par un humain (ou un LLM)
à partir du DAG, des traces, et des scores ternaires.

## Usage

```bash
explain-anything narrative  --dag causal_dag.json --node N1
explain-anything summary    --dag causal_dag.json
explain-anything query      --dag causal_dag.json --question "Pourquoi X a-t-il drifté ?"
explain-anything export     --dag causal_dag.json --output explanation.json
```

## Strate

L2/L3 hybride — génération de texte structuré (L2) + données causales (L3).
READ-ONLY : ne modifie jamais le DAG.

---

*IntentHash: 0xCTULU_EXPLAIN_ANYTHING_20260612*
*PRD: PRD-056-multirepos-agentique-2026-06-07.md*
*[CONFORME_NEXUS]*
