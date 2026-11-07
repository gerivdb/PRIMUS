#!/usr/bin/env pwsh
# ============================================================================
# wal-merkle-tracker.ps1 - Primitive de tracabilite Merkle WAL
# Empreinte WAL : 0x243
#
# Génère un hash SHA256 à partir d'un fichier ou d'une chaîne,
# et l'écrit dans un fichier WAL JSON (append-only).
# ============================================================================
param(
    [Parameter(Mandatory=$false)]
    [string]$chemin,
    [Parameter(Mandatory=$false)]
    [string]$contenu,
    [Parameter(Mandatory=$false)]
    [string]$walId = "WAL-0x243",
    [Parameter(Mandatory=$false)]
    [string]$walFile = "WAL/0x243-merkle-wal.json"
)

$ErrorActionPreference = "Stop"

# --- Déterminer le contenu à hasher ---
if ($PSBoundParameters.ContainsKey('chemin')) {
    if (-not (Test-Path $chemin)) {
        Write-Error "Fichier introuvable : $chemin"
        exit 1
    }
    $hash = Get-FileHash -Path $chemin -Algorithm SHA256
    $hashValue = $hash.Hash
    $operation = "hash_file"
    $source = $chemin
} elseif ($PSBoundParameters.ContainsKey('contenu')) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($contenu)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $hashBytes = $sha.ComputeHash($bytes)
    $hashValue = [BitConverter]::ToString($hashBytes).Replace("-", "").ToLower()
    $operation = "hash_string"
    $source = $contenu.Substring(0, [Math]::Min(50, $contenu.Length))
} else {
    Write-Error "Vous devez spécifier -chemin ou -contenu"
    exit 1
}

# --- Écrire dans le fichier WAL ---
$timestamp = (Get-Date).ToUniversalTime().ToString("o")
$entry = @{
    timestamp = $timestamp
    operation = $operation
    walId     = $walId
    hash      = $hashValue
    type      = "sha256"
    source    = $source
} | ConvertTo-Json -Depth 3

$dir = Split-Path $walFile -Parent
if ($dir -and -not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

if (Test-Path $walFile) {
    $contenuExist = Get-Content $walFile -Raw
    if ($contenuExist.Trim()) {
        $json = $contenuExist | ConvertFrom-Json
        if (-not $json) { $json = @() }
        $json += $entry
        $json | ConvertTo-Json -Depth 5 | Set-Content -Path $walFile -Encoding UTF8
    } else {
        @($entry) | ConvertTo-Json -Depth 5 | Set-Content -Path $walFile -Encoding UTF8
    }
} else {
    @($entry) | ConvertTo-Json -Depth 5 | Set-Content -Path $walFile -Encoding UTF8
}

Write-Output $hashValue
Write-Output "WAL écrit : $walFile"
