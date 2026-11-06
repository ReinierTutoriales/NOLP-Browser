#!/usr/bin/env python3
"""Generate NOLP application icons from the canonical transparent SVG.

Dependencies: pip install cairosvg pillow
No network requests are made by this script. SVG source is repository-owned.
"""
from __future__ import annotations
import argparse
import io
from pathlib import Path

SIZES = (16, 24, 32, 48, 64, 128, 192, 256, 512, 1024, 2048)
ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)


def build(source: Path, output: Path) -> None:
    import cairosvg
    from PIL import Image

    output.mkdir(parents=True, exist_ok=True)
    png_dir = output / "png"
    png_dir.mkdir(exist_ok=True)
    svg = source.read_bytes()
    images = {}
    for size in SIZES:
        data = cairosvg.svg2png(bytestring=svg, output_width=size, output_height=size)
        img = Image.open(io.BytesIO(data)).convert("RGBA")
        if img.size != (size, size):
            raise ValueError(f"Unexpected icon dimensions: {img.size}")
        if img.getpixel((0, 0))[3] != 0:
            raise ValueError("Source icon is not transparent in corners")
        img.save(png_dir / f"nolp-{size}.png", optimize=True)
        images[size] = img
    # Pillow writes multi-resolution ICO and ICNS without platform-specific tools.
    images[256].save(output / "nolp.ico", format="ICO",
                     sizes=[(n, n) for n in ICO_SIZES])
    images[1024].save(output / "nolp.icns", format="ICNS",
                      append_images=[images[512], images[256], images[128], images[64], images[32], images[16]])
    # Linux desktop icon: scalable source plus freedesktop.org hicolor PNG hierarchy.
    scalable = output / "linux" / "hicolor" / "scalable" / "apps"
    scalable.mkdir(parents=True, exist_ok=True)
    (scalable / "nolp.svg").write_bytes(svg)
    for size in (16, 24, 32, 48, 64, 128, 256, 512):
        directory = output / "linux" / "hicolor" / f"{size}x{size}" / "apps"
        directory.mkdir(parents=True, exist_ok=True)
        images[size].save(directory / "nolp.png")
    # Android: transparent foreground; adaptive background and monochrome need
    # separately designed platform-specific resources, not a fake generated mask.
    android = output / "android" / "foreground"
    android.mkdir(parents=True, exist_ok=True)
    images[512].save(android / "nolp-foreground.png")
    # Web/PWA favicon source and portable high-DPI PNG.
    web = output / "web"
    web.mkdir(exist_ok=True)
    (web / "favicon.svg").write_bytes(svg)
    for size in (32, 192, 512):
        images[size].save(web / f"nolp-{size}.png")
    print(f"Generated icon pack in {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("assets/brand/nolp-icon.svg"))
    parser.add_argument("--output", type=Path, default=Path("dist/nolp-icons"))
    args = parser.parse_args()
    build(args.source, args.output)
