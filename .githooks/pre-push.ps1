#!/usr/bin/env pwsh
# Shard PRIMUS pre-push implementation
param([Parameter(ValueFromRemainingArguments=$true)][string[]]$HookArgs)

if ($HookArgs -contains '--force') {
    Write-Host "PRE-PUSH REJECTED: --force interdit (utilisez --force-with-lease)"
    exit 1
}
exit 0
