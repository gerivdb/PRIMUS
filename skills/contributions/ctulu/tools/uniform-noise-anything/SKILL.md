# uniform-noise-anything — Uniform State Diffusion pour DAGs CTULU

## Description

Inspiré de **UDLM (Uniform State Diffusion)** [DiffusionGemma Ch.3], injecte dans
les nœuds inconnus d'un DAG une **valeur plausible-mais-incorrecte** tirée du
schéma connu, forçant les outils aval à corriger activement.

## Modes de bruit

| Mode | Comportement | Analogue |
|------|-------------|----------|
| `absorbing` | nœud = null (legacy) | MDLM — état masque |
| `uniform` | nœud = valeur aléatoire du schéma | UDLM — bruit uniforme |
| `plausible` | nœud = valeur fausse mais vraisemblable | UDLM guidé |
| `adversarial` | nœud = valeur maximalement conflictuelle | stress test |

## Usage

```bash
# Injection UDLM sur tous les nœuds inconnus
uniform-noise-anything inject --dag EPIC-245.dag --mode uniform

# Injection ciblée sur nœuds spécifiques
uniform-noise-anything inject --dag EPIC-245.dag --mode plausible --nodes N7,N9

# Cycle complet inject→denoise→compare
uniform-noise-anything denoise --dag noisy.dag --tool cause-anything
uniform-noise-anything compare --clean EPIC-245.dag --noisy noisy.dag

# Stress test adversarial
uniform-noise-anything stress --dag EPIC-245.dag --mode adversarial
```

## Output

Le rapport d'injection liste les nœuds injectés, les corrections appliquées,
les dépendances implicites révélées, et le score de stress du DAG.

## Strate

L3 — algorithme pur, zéro dépendance externe, zéro GPU.
Exécutable immédiatement sur ENV2.

---

*IntentHash: 0xCTULU_UNIFORM_NOISE_ANYTHING_φ6.881*
*PRD: PRD-050-v1-uniform-noise-anything.md*
*[CONFORME_NEXUS]*
