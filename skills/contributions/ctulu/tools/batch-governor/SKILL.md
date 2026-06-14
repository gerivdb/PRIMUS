# batch-governor — Gates BRGS Automatiques P0→4

## Description
Pipeline bloquant avant tout push de batch. 5 gates séquentiels avec HALT au premier échec.

## Usage
```bash
# Dry-run (simulation)
python governor.py run --batch-dir ./batch_output/ --mode dry_run

# Execute (push si gates passent)
python governor.py run --batch-dir ./batch_output/ --mode execute

# Audit rétroactif
python governor.py audit --batch-dir ./batch_12/

# Rapport
python governor.py report --batch-dir ./batch_output/ --format yaml
```

## Gates
| Gate | Name | Rule | On Fail |
|------|------|------|---------|
| GATE-0 | known_repositories_check | Tous les repo_cible existent dans known_repositories.yaml | HALT |
| GATE-1 | intent_hash_uniqueness | 0 collision IntentHash dans registry.yaml | HALT |
| GATE-2 | dep_graph_acyclic | DAG sans cycle | HALT + cycles |
| GATE-3 | phi_cps_threshold | φ-CPS ≥ 4.559 | HALT + sous-seuil |
| GATE-4 | index_cleanup_completeness | 100% EPICs mappés dans delta | HALT |

## Modes
- `dry_run` : Simule les 5 gates, émet rapport, 0 écriture
- `execute` : Passe gates → autorise push si OK
- `audit` : Rejoue les gates sur batch déjà mergé

## Strate
L3 (DevTools) — guard pur. Sources : L0+L1.
