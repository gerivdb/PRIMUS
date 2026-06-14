# holograph-anything — Propagateur Causal L0→L9

## Description
Écoute les événements du cycle de vie et propage leurs effets causaux à travers L0→L9 bidirectionnellement.

## Usage
```bash
python propagation_engine.py watch --repo gerivdb/GOVERNANCE-HUB
python propagation_engine.py trigger --event EPIC_completed --epic EPIC-249
python propagation_engine.py trigger --event ADR_accepted --adr ADR-068
python propagation_engine.py status
```

## Événements
| Event | Propagations |
|-------|-------------|
| EPIC_completed | index → ROADMAP → deps downstream → φ-CPS |
| ADR_accepted | tag EPICs → KEEL-CONFORMANCE → BRIDGES |
| merge_to_main | snapshot NEXUS → drift reset → φ-CPS |
| branch_created | register repos → BRGS routing |
| KEEL_rule_added | scan EPICs → tag compliance |

## Escalade HITL si δφ-CPS > 0.5

## Strate
L2/L3 hybride — seul tool opérant sur toutes les strates.
