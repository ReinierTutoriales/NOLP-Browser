#!/usr/bin/env bash
# Headless Gecko rendering smoke; validates upstream Firefox, not NOLP product integration.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TREE="${NOLP_FIREFOX_DIR:-$ROOT/.upstream/firefox}"
if [[ ! -x "$TREE/mach" ]]; then
  echo "Firefox source missing: $TREE" >&2
  exit 2
fi
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/profile"
cat > "$WORK/page.html" <<'HTML'
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>NOLP Gecko smoke</title></head>
<body style="background:#fff;color:#000"><h1>Gecko rendering smoke</h1></body>
</html>
HTML
# --screenshot exits after rendering; timeout prevents CI from hanging indefinitely.
cd "$TREE"
timeout 90s ./mach run --headless --no-remote --profile "$WORK/profile" \
  --window-size 800,600 --screenshot "$WORK/render.png" "file://$WORK/page.html"
python3 - "$WORK/render.png" <<'PY'
import pathlib
import struct
import sys
p = pathlib.Path(sys.argv[1])
data = p.read_bytes()
if len(data) < 100 or data[:8] != b"\x89PNG\r\n\x1a\n":
    raise SystemExit("Gecko did not produce a valid PNG screenshot")
width, height = struct.unpack(">II", data[16:24])
if width < 100 or height < 100:
    raise SystemExit(f"Unexpected Gecko screenshot dimensions: {width}x{height}")
print(f"Gecko rendered a local HTML document: {width}x{height}, {len(data)} bytes")
PY
