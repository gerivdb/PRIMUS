# SKILL.md — CTULU narrative-engine

## Description
Moteur narratif générique extrait de HOLMES. Orchestre la génération d'une histoire à partir d'événements bruts, valide le lore via un validator pluggable, et rend le résultat en markdown via un générateur abstrait.

## Usage

```python
from narrative_engine import NarrativeEngine, LoreValidator

engine = NarrativeEngine(lore=MonLoreValidator())
story = engine.generate(
    title="The Adventure of the Empty House",
    characters=["holmes", "watson"],
    raw_events=[...],
    year=1894,
    style="watson_pov",
)
print(story.output_md)
```

## Architecture

```
CTULU/tools/narrative-engine/
  types.py              ← NarrativeEvent, Clue, Hypothesis, Story
  lore_interface.py     ← LoreValidator (ABC) + LoreConstraint (ABC)
  generation_engine.py  ← GenerationEngine (ABC) + dispatch squelette
  narrative_engine.py   ← NarrativeEngine (orchestrateur générique)
  tool.yaml             ← Manifeste outil
  SKILL.md              ← Ce fichier
```

## Pattern Strategy

- `LoreValidator` : injecter une implémentation spécifique (HOLMES victorien, BATVERSE dramatique, etc.)
- `GenerationEngine` : injecter un rendu spécifique (Watson POV, telegramme, etc.)
- `NarrativeEngine` : orchestrateur générique, aucun lore ni template hardcodé

## Références

- **EPIC-0008** : Extraction moteur narratif vers CTULU
- **HOLMES/src/core/types.py** : source initiale des types
- **HOLMES/src/engines/narrative_engine.py** : source initiale orchestrateur
- **ADR-044** : [CONFORME_NEXUS] — Extraction narrative-engine-core vers CTULU
