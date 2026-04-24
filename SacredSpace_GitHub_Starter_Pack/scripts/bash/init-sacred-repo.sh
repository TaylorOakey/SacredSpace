#!/usr/bin/env bash
set -euo pipefail
REPO_NAME="${1:-SacredSpace_Repo}"
TARGET_ROOT="${2:-.}"
REPO_PATH="$TARGET_ROOT/$REPO_NAME"
mkdir -p "$REPO_PATH"/{.github/ISSUE_TEMPLATE,.github/workflows,docs/canon,docs/governance,agents,templates,scripts/powershell,scripts/bash,config/labels}
if [ ! -d "$REPO_PATH/.git" ]; then
  git -C "$REPO_PATH" init
fi
echo "Initialized $REPO_PATH"
