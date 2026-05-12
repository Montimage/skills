#!/usr/bin/env bash
# detect_ecosystems.sh — identify which package/CI ecosystems are present in a repo.
#
# Prints one line per detected ecosystem to stdout:
#   npm <lockfile-name>
#   python <primary-manager>
#   docker <dockerfile-path>
#   github-actions <workflow-count>
#
# Exit codes:
#   0 — at least one ecosystem detected, listed on stdout
#   2 — no supported ecosystem present (descriptive message on stderr)
#   3 — not inside a git repository (descriptive message on stderr)

set -euo pipefail

root="${1:-.}"

if [ ! -d "$root" ]; then
  echo "Error: directory '$root' does not exist." >&2
  echo "Usage: detect_ecosystems.sh [path]   (defaults to current directory)" >&2
  exit 3
fi

cd "$root"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Error: '$root' is not inside a git repository." >&2
  echo "The supply-chain-audit skill requires git so it can show diffs before applying changes." >&2
  exit 3
fi

found=0

# --- npm / pnpm / yarn ---
npm_lock=""
for f in package-lock.json pnpm-lock.yaml yarn.lock bun.lockb; do
  if [ -f "$f" ]; then
    if [ -n "$npm_lock" ]; then
      echo "npm multiple-lockfiles:$npm_lock,$f"
    else
      npm_lock="$f"
    fi
  fi
done
if [ -n "$npm_lock" ]; then
  echo "npm $npm_lock"
  found=1
elif [ -f package.json ]; then
  echo "npm no-lockfile"
  found=1
fi

# --- Python ---
py_manager=""
if [ -f uv.lock ]; then
  py_manager="uv"
elif [ -f poetry.lock ]; then
  py_manager="poetry"
elif [ -f Pipfile.lock ]; then
  py_manager="pipenv"
elif [ -f pdm.lock ]; then
  py_manager="pdm"
elif ls requirements*.txt >/dev/null 2>&1; then
  py_manager="pip"
elif [ -f pyproject.toml ] || [ -f setup.py ] || [ -f setup.cfg ]; then
  py_manager="pip-legacy"
fi
if [ -n "$py_manager" ]; then
  echo "python $py_manager"
  found=1
fi

# --- Docker ---
df_paths=""
while IFS= read -r df; do
  df_paths="${df_paths}${df_paths:+,}${df}"
done < <(find . -maxdepth 3 -type f \( -name 'Dockerfile' -o -name 'Dockerfile.*' \) 2>/dev/null | sed 's|^\./||')

compose_paths=""
while IFS= read -r cf; do
  compose_paths="${compose_paths}${compose_paths:+,}${cf}"
done < <(find . -maxdepth 2 -type f \( -name 'docker-compose.yml' -o -name 'docker-compose.yaml' -o -name 'compose.yml' -o -name 'compose.yaml' \) 2>/dev/null | sed 's|^\./||')

if [ -n "$df_paths" ] || [ -n "$compose_paths" ]; then
  echo "docker dockerfiles=${df_paths:-none} compose=${compose_paths:-none}"
  found=1
fi

# --- GitHub Actions ---
if [ -d .github/workflows ]; then
  wf_count=$(find .github/workflows -maxdepth 1 -type f \( -name '*.yml' -o -name '*.yaml' \) 2>/dev/null | wc -l | tr -d ' ')
  if [ "$wf_count" -gt 0 ]; then
    echo "github-actions $wf_count"
    found=1
  fi
fi

if [ "$found" -eq 0 ]; then
  echo "No supported ecosystem detected in '$root'." >&2
  echo "Supported triggers: package.json, pyproject.toml/requirements*.txt, Dockerfile, .github/workflows/*.y*ml" >&2
  exit 2
fi

exit 0
