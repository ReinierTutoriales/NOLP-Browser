#!/usr/bin/env bash
# Development launcher for pinned upstream Firefox. Not a branded NOLP browser.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TREE="${NOLP_FIREFOX_DIR:-$ROOT/.upstream/firefox}"
URL="${1:-about:blank}"
if [[ $# -gt 1 ]]; then
  echo "Usage: bash scripts/run-nolp-desktop.sh [https-url|about:blank]" >&2
  exit 2
fi
if [[ "$URL" != "about:blank" && ! "$URL" =~ ^https://[A-Za-z0-9] ]]; then
  echo "Only HTTPS URLs and about:blank are accepted by the development launcher" >&2
  exit 2
fi
if [[ ! -x "$TREE/mach" ]]; then
  echo "Pinned Firefox source unavailable at $TREE" >&2
  exit 3
fi
EXPECTED="$(python3 - "$ROOT/engine/upstream-manifest/firefox.toml" <<'PY'
import sys, tomllib
with open(sys.argv[1], "rb") as f:
    print(tomllib.load(f)["firefox"]["revision"])
PY
)"
ACTUAL="$(git -C "$TREE" rev-parse HEAD)"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "Firefox revision mismatch: refusing to run unverified engine" >&2
  exit 4
fi
if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
  echo "Graphical Linux session required (DISPLAY or WAYLAND_DISPLAY)" >&2
  exit 5
fi
PROFILE="${NOLP_DEV_PROFILE:-$ROOT/.local/nolp-desktop-profile}"
mkdir -p "$PROFILE"
chmod 700 "$PROFILE"
echo "Launching pinned upstream Firefox with isolated development profile: $PROFILE"
cd "$TREE"
exec ./mach run --no-remote --profile "$PROFILE" "$URL"
