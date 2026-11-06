#!/usr/bin/env bash
set -euo pipefail
# NOLP bootstrap: clone only an explicitly pinned upstream revision.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REV="${FIREFOX_REVISION:-}"
DEST="${NOLP_FIREFOX_DIR:-$ROOT/.upstream/firefox}"
if [[ -z "$REV" || ! "$REV" =~ ^[0-9a-fA-F]{40}$ ]]; then
  echo "Set FIREFOX_REVISION to a reviewed, immutable 40-character Firefox commit SHA." >&2
  exit 2
fi
if [[ -e "$DEST" ]]; then
  echo "Destination already exists: $DEST (refusing to overwrite)" >&2
  exit 3
fi
mkdir -p "$(dirname "$DEST")"
git clone --filter=blob:none https://github.com/mozilla-firefox/firefox.git "$DEST"
git -C "$DEST" checkout --detach "$REV"
test "$(git -C "$DEST" rev-parse HEAD)" = "${REV,,}"
printf 'Firefox source checked out at %s\n' "$DEST"
printf 'Next: install upstream build prerequisites and follow Mozilla build instructions.\n'
