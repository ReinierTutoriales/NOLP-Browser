#!/usr/bin/env python3
"""Create an independent NOLP branding directory from pinned Firefox unofficial branding.

Keep upstream packaging metadata intact; replace brand strings and PNG artwork.
Never mutate Mozilla's official branding or source assets.
"""
import argparse
from pathlib import Path
import re
import shutil

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/brand/nolp-official.png"
UPSTREAM = Path("browser/branding/unofficial")
TARGET = Path("browser/branding/nolp")
TERMS = {
    "-brand-shorter-name": "NOLP",
    "-brand-short-name": "NOLP",
    "-brand-shortcut-name": "NOLP",
    "-brand-full-name": "NOLP",
    "-brand-product-name": "NOLP",
    "-vendor-short-name": "NOLP",
}


def install(root: Path, check: bool = False) -> None:
    upstream, target = root / UPSTREAM, root / TARGET
    if not upstream.is_dir() or not SOURCE.is_file():
        raise ValueError("Pinned Firefox unofficial branding or official NOLP artwork missing")
    if not check and not target.exists():
        shutil.copytree(upstream, target)
    if not target.is_dir():
        raise ValueError("NOLP branding directory missing")

    # Branding names are localized via Fluent, not by replacing text across Gecko.
    fluent = list(target.rglob("brand.ftl"))
    if not fluent:
        raise ValueError("No brand.ftl found in upstream branding")
    for path in fluent:
        data = path.read_text(encoding="utf-8")
        for term, value in TERMS.items():
            pattern = rf"(?m)^(\s*{re.escape(term)}\s*=).*$"
            if not re.search(pattern, data):
                raise ValueError(f"Missing {term} in {path}")
            data = re.sub(pattern, lambda m: f"{m.group(1)} {value}", data, count=1)
        if check:
            if path.read_text(encoding="utf-8") != data:
                raise ValueError(f"Incorrect NOLP brand terms in {path}")
        else:
            path.write_text(data, encoding="utf-8")

    # Firefox's application display name is configured separately from Fluent.
    config = target / "configure.sh"
    configuration = config.read_text(encoding="utf-8")
    configuration = re.sub(r"(?m)^MOZ_APP_DISPLAYNAME=.*$", "MOZ_APP_DISPLAYNAME=NOLP", configuration)
    configuration = re.sub(r"(?m)^MOZ_MACBUNDLE_ID=.*$", "MOZ_MACBUNDLE_ID=org.nolp.browser", configuration)
    if check:
        if config.read_text(encoding="utf-8") != configuration:
            raise ValueError("NOLP application display name or bundle ID incorrect")
    else:
        config.write_text(configuration, encoding="utf-8")

    properties = target / "locales/en-US/brand.properties"
    if properties.is_file():
        old = properties.read_text(encoding="utf-8")
        updated = old.replace("Nightly", "NOLP").replace("Firefox", "NOLP")
        if check:
            if old != updated:
                raise ValueError("NOLP legacy brand.properties not installed")
        else:
            properties.write_text(updated, encoding="utf-8")

    # Keep package metadata consistent with the selected brand.
    for name in ("branding.nsi",):
        file = target / name
        if file.is_file():
            data = file.read_text(encoding="utf-8")
            # Do not globally rewrite Mozilla installer directives: they
            # include paths and identifiers which are not product labels.
            if check and not data:
                raise ValueError(f"Empty branding metadata: {file}")

    # Original icon is centered in its own transparent canvas. Crop alpha bounds
    # once and retain 2.5% safety inset, then downsample with Lanczos.
    with Image.open(SOURCE) as raw:
        image = raw.convert("RGBA")
    bounds = image.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("Official NOLP logo has no visible pixels")
    image = image.crop(bounds)
    # Only application icons: do not overwrite private browsing, installer art,\n    # tile backgrounds, or unrelated PNG resources.\n    icons = sorted(target.glob("default[0-9]*.png"))
    if not icons:
        raise ValueError("No PNG assets in Firefox unofficial branding")
    for path in icons:
        with Image.open(path) as original:
            width, height = original.size
        if width != height:
            continue  # Never overwrite non-square artwork or platform-specific banners.
        side = min(width, height)
        margin = max(1, round(side * .025)) if side >= 32 else 0
        available = side - 2 * margin
        scale = min(available / image.width, available / image.height)
        scaled = image.resize((max(1, round(image.width * scale)),
                               max(1, round(image.height * scale))), Image.Resampling.LANCZOS)
        output = Image.new("RGBA", (width, height))
        output.alpha_composite(scaled, ((width - scaled.width) // 2, (height - scaled.height) // 2))
        if check:
            with Image.open(path) as existing:
                if existing.convert("RGBA").tobytes() != output.tobytes():
                    raise ValueError(f"Incorrect NOLP artwork in {path}")
        else:
            output.save(path, optimize=True)
    # Firefox also packages native ICO/ICNS assets. Do not silently ship
    # Mozilla icons under the NOLP name: require dedicated conversion before
    # treating Windows/macOS branding as complete.
    # Windows executable icon and macOS application icon, using the same
    # official source. Other icon roles retain their original specialized art.
    for name in ("firefox.ico", "firefox64.ico"):
        dest = target / name
        if dest.is_file():
            from io import BytesIO
            buffer = BytesIO()
            canvas = Image.new("RGBA", (256, 256))
            fitted = image.copy()
            fitted.thumbnail((244, 244), Image.Resampling.LANCZOS)
            canvas.alpha_composite(fitted, ((256 - fitted.width) // 2, (256 - fitted.height) // 2))
            canvas.save(buffer, format="ICO", sizes=[(n, n) for n in (16, 24, 32, 48, 64, 128, 256)])
            payload = buffer.getvalue()
            if check:
                if dest.read_bytes() != payload:
                    raise ValueError(f"NOLP Windows icon not installed: {name}")
            else:
                dest.write_bytes(payload)
    mac = target / "firefox.icns"
    if mac.is_file():
        from io import BytesIO
        buffer = BytesIO()
        icon = Image.new("RGBA", (1024, 1024))
        fitted = image.copy()
        fitted.thumbnail((972, 972), Image.Resampling.LANCZOS)
        icon.alpha_composite(fitted, ((1024 - fitted.width) // 2, (1024 - fitted.height) // 2))
        icon.save(buffer, format="ICNS")
        if check:
            if mac.read_bytes() != buffer.getvalue():
                raise ValueError("NOLP macOS icon not installed")
        else:
            mac.write_bytes(buffer.getvalue())
    print("Note: macOS Assets.car and specialized document/private icons remain upstream")
    print(f"NOLP branding {'verified' if check else 'installed'}: {target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--firefox-dir", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    install(args.firefox_dir, args.check)
