# kv-cache-anything — Shared Context Cache Inter-Outils

## Description

Inspiré du **KV-Cache Sharing** de DiffusionGemma [Ch.4], implémente un cache
de contextes partagé entre outils CTULU au sein d'une session batch.
Le contexte L0 est chargé une fois, puis toutes les lectures ultérieures
sont servies depuis le cache local.

## Architecture

```
Session batch → [init] → Cache local (TTL configurable)
                    ├── outil-1 : get_context → HIT (0ms)
                    ├── outil-2 : get_context → HIT (0ms)
                    └── outil-N : get_context → HIT (0ms)
Fin session → cache invalidé
```

## TTL par niveau

| Niveau | Ressource | TTL |
|--------|-----------|-----|
| L0 | known_repositories, KEEL, AGENT_RAM | 1h |
| L1 | README, tool.yaml | 30min |
| L2 | Contenu de fichiers | 10min |

## Usage

```bash
kv-cache-anything init  --session batch-13 --repos gerivdb/GOVERNANCE-HUB
kv-cache-anything get   --key known_repositories --session batch-13
kv-cache-anything set   --key README/NEXUS --value @file.md --ttl 3600
kv-cache-anything stats --session batch-13
kv-cache-anything warm  --session batch-13 --level L0
kv-cache-anything flush --session batch-13
```

## Strate

L3 — infrastructure de cache locale, zéro GPU, zéro API externe.

---

*IntentHash: 0xCTULU_KV_CACHE_ANYTHING_φ6.234*
*PRD: PRD-052-v1-kv-cache-anything.md*
*[CONFORME_NEXUS]*
