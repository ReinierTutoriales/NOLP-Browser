#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$ROOT/engine/upstream-manifest/firefox.toml"
REV="$(python3 - "$MANIFEST" <<'PY'
import sys,tomllib
with open(sys.argv[1],"rb") as f: print(tomllib.load(f)["firefox"]["revision"])
PY
)"
if [[ ! "$REV" =~ ^[0-9a-f]{40}$ ]]; then
  echo "Invalid Firefox revision in manifest" >&2; exit 2
fi
if [[ -n "${FIREFOX_REVISION:-}" && "${FIREFOX_REVISION,,}" != "$REV" ]]; then
  echo "FIREFOX_REVISION does not match the pinned manifest; refusing unreviewed revision" >&2; exit 2
fi
DEST="${NOLP_FIREFOX_DIR:-$ROOT/.upstream/firefox}"
if [[ -e "$DEST" ]]; then echo "Destination exists: $DEST" >&2; exit 3; fi
mkdir -p "$(dirname "$DEST")"
git clone --filter=blob:none --no-checkout https://github.com/mozilla-firefox/firefox.git "$DEST"
git -C "$DEST" checkout --detach "$REV"
test "$(git -C "$DEST" rev-parse HEAD)" = "$REV"
printf 'Pinned Firefox upstream: %s\n' "$REV"
