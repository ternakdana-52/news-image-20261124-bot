#!/usr/bin/env python3
"""Write the 24 November 2026 world-news image to /output/entry.png.

The image is the entry.png beside this file, composed with PIL from six
verified news stories of Tuesday 24 November 2026. This program copies it
byte for byte, so every run writes the same bytes. Standard library only,
no network, no randomness, no timestamps.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    os.chmod(DST, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
