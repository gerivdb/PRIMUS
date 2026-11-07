---
type: PRIMITIVE
version: 1.0.0
intent_hash: 0xPRIMITIVE_WAL_MERKLE_TRACKER_20261105
---

# Primitive : wal-merkle-tracker

## Rôle
Générer un hash SHA256 (Merkle root) à partir d'un fichier ou d'une chaîne, et l'écrire dans un fichier WAL JSON pour traçabilité (Proof-of-Life).

## Entrée
- `chemin` : chemin vers un fichier à hasher (optionnel)
- `contenu` : chaîne à hasher directement (optionnel, alternative à `chemin`)
- `walId` : identifiant WAL (défaut `WAL-0x243`)
- `walFile` : chemin du fichier WAL JSON de sortie (défaut `WAL/0x243-merkle-wal.json`)

## Sortie
- Fichier WAL JSON mis à jour avec l'entrée : `{ timestamp, operation, walId, hash, type, ... }`
- Affichage du hash sur stdout

## Implémentation
PowerShell natif (`Get-FileHash -Algorithm SHA256`).

## Contraintes
- Un seul hash par appel
- Le fichier WAL est append-only (ajout d'entrée)
- Aucun appel réseau

## Exemple
```powershell
.\wal-merkle-tracker.ps1 -chemin "gas_scripts/sync-veille-to-google-services.gs" -walId "WAL-0x243"
```
