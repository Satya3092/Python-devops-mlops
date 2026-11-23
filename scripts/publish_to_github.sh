#!/usr/bin/env bash
# Publish this repository to GitHub in one step.
# Usage: bash scripts/publish_to_github.sh [repo-name] [public|private]
# Requires git; uses the GitHub CLI (https://cli.github.com) if installed (run 'gh auth login' first).
set -euo pipefail

REPO_NAME="${1:-100-days-python-devops-mlops}"
VISIBILITY="${2:-public}"
DESCRIPTION="100-day hands-on Python course: from absolute beginner to DevOps automation, data analysis, ML and MLOps"

cd "$(dirname "$0")/.."
git rev-parse --git-dir >/dev/null 2>&1 || git init -b main
git add .
git commit -m "Initial commit: 100 Days of Python - From Beginner to DevOps and MLOps" || echo "Nothing new to commit"

if command -v gh >/dev/null 2>&1; then
  gh repo create "$REPO_NAME" "--$VISIBILITY" --source . --remote origin --push --description "$DESCRIPTION"
  gh repo edit --add-topic python,devops,mlops,100daysofcode,automation,machine-learning,fastapi,docker,boto3,pandas
  echo "Done: $(gh repo view --json url -q .url)"
else
  echo "GitHub CLI not found. Create an EMPTY repository named '$REPO_NAME' on https://github.com/new"
  echo "(no README, no .gitignore, no license), then run:"
  echo "  git remote add origin https://github.com/<your-username>/$REPO_NAME.git"
  echo "  git push -u origin main"
fi
