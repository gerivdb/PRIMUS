#!/bin/sh
# install-hooks.sh — PRIMUS
# Active les githooks du repo
# Usage: sh .githooks/install-hooks.sh

git config core.hooksPath .githooks
echo '[PRIMUS] Hooks actives: .githooks/'
echo '  - pre-commit: RSS-v2 lint + contrat primitives + encoding'
