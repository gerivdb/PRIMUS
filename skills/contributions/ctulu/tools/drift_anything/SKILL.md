# drift-anything — Sentinelle de Drift Structurel

## Description
Détecte les écarts entre l'intention déclarée et l'état réel. 3 types de drift.

## Usage
```bash
python drift_scanner.py scan --repo gerivdb/GOVERNANCE-HUB
python drift_scanner.py scan --type structural
python drift_scanner.py watch --daemon
python drift_scanner.py report --format yaml
python drift_scanner.py delta --since batch-11
```

## Types de drift
| Type | Détection |
|------|-----------|
| Structural | Status ≠ livrable, known_repos ≠ GitHub, KEEL ≠ hooks |
| Semantic | ADR sans implémentation, EPIC sans activité |
| Causal | Dep inversée, IntentHash absent |

## Score : 0 (parfait) → 100 (chaos)

## Strate
L2/L3 hybride — analyse cognitive + exécution surveillance.
