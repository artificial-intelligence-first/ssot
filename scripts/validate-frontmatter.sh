#!/usr/bin/env bash
# Simple frontmatter validator for Markdown files under docs/

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${ROOT_DIR}/docs"

missing=0

while IFS= read -r -d '' file; do
  echo "Checking ${file#${ROOT_DIR}/}..."

  frontmatter="$(awk '
    NR==1 && $0=="---" {in_frontmatter=1; next}
    in_frontmatter && $0=="---" {exit}
    in_frontmatter {print}
  ' "$file")"

  if [[ -z "$frontmatter" ]]; then
    echo "  ERROR: Missing frontmatter block"
    missing=1
    continue
  fi

  for field in title slug status last_updated tags summary; do
    if ! grep -q "^${field}:" <<<"$frontmatter"; then
      echo "  ERROR: Missing ${field}"
      missing=1
    fi
  done
done < <(find "$TARGET_DIR" -name "*.md" -print0)

if ((missing)); then
  echo "Frontmatter validation failed."
  exit 1
fi

echo "Frontmatter validation passed."
