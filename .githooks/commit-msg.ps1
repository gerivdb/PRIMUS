#!/usr/bin/env pwsh
# Shard PRIMUS commit-msg implementation
param([Parameter(ValueFromRemainingArguments=$true)][string[]]$HookArgs)

if ($HookArgs -and $HookArgs[0]) {
    $msgFile = $HookArgs[0]
    $msg = Get-Content $msgFile -Raw
    if ($msg.Length -lt 10) {
        Write-Host "COMMIT-MSG REJECTED: message trop court (< 10 chars)"
        exit 1
    }
    if ($msg -match '<placeholder>') {
        Write-Host "COMMIT-MSG REJECTED: placeholder détecté"
        exit 1
    }
}
exit 0
