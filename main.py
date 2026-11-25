#!/usr/bin/env python3
"""Write the 24 November 2026 world-news image to /output/entry.png.

The image is the entry.png beside this file, composed with PIL from six
verified news stories of Tuesday 24 November 2026. This program copies it
byte for byte, so every run writes the same bytes. Standard library only,
no network, no randomness, no timestamps.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")

MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def png_size(path):
    """Return (width, height) of a PNG from its IHDR chunk, or None."""
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main() -> int:
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1
    dims = png_size(SRC)
    if dims is None or dims[0] > MAX_SIDE or dims[1] > MAX_SIDE:
        print(f"entry.png dimensions {dims} are not within 1024x1024", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    os.chmod(DST, 0o644)
    # Verify the copy is byte-for-byte identical to the source image.
    with open(SRC, "rb") as f:
        src_hash = hashlib.sha256(f.read()).hexdigest()
    with open(DST, "rb") as f:
        dst_hash = hashlib.sha256(f.read()).hexdigest()
    if src_hash != dst_hash:
        print("copied entry.png does not match the source image", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
