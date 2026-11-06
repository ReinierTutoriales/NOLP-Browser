#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TREE="${NOLP_FIREFOX_DIR:-$ROOT/.upstream/firefox}"
if [[ ! -x "$TREE/mach" ]]; then
  echo "Firefox source missing: run bash scripts/bootstrap-firefox.sh" >&2
  exit 2
fi
EXPECTED="$(python3 - "$ROOT/engine/upstream-manifest/firefox.toml" <<'PY'
import sys,tomllib
with open(sys.argv[1],"rb") as f: print(tomllib.load(f)["firefox"]["revision"])
PY
)"
ACTUAL="$(git -C "$TREE" rev-parse HEAD)"
if [[ "$EXPECTED" != "$ACTUAL" ]]; then
  echo "Upstream mismatch: expected $EXPECTED, found $ACTUAL" >&2
  exit 3
fi
VERSION="$(python3 - "$ROOT/engine/upstream-manifest/firefox.toml" <<'PY'
import sys,tomllib
with open(sys.argv[1],"rb") as f: print(tomllib.load(f)["firefox"]["version"])
PY
)"
ACTUAL_VERSION="$(tr -d '\\r\\n' < "$TREE/browser/config/version.txt")"
if [[ "$ACTUAL_VERSION" != "$VERSION" ]]; then
  echo "Upstream version mismatch: expected $VERSION, found $ACTUAL_VERSION" >&2
  exit 4
fi
echo "Verified Gecko source revision: $ACTUAL ($ACTUAL_VERSION)"
if [[ "${NOLP_RUN_BUILD:-0}" == "1" ]]; then
  (cd "$TREE" && ./mach build)
else
  echo "Source verified; no build executed. Set NOLP_RUN_BUILD=1 to build."
fi
