#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261123 bounty.

It ships the finished front-page picture: it checks the bundled
``entry.png`` is a real, in-limits PNG and copies it to the output path
the grader reads, ``/output/entry.png`` (or ``$MAKEFUN_OUTPUT_DIR`` when
the harness sets one). No network, no clock, no randomness, so two runs
write the same bytes.
"""

import binascii
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def fail(message):
    print("error:", message, file=sys.stderr)
    raise SystemExit(1)


def check_png(data):
    if len(data) < 33:
        fail("entry.png is too short to be a PNG")
    if data[:8] != PNG_MAGIC:
        fail("entry.png does not start with the PNG magic bytes")
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk where one belongs")
    ihdr = data[12:29]
    stored_crc, = struct.unpack(">I", data[29:33])
    if binascii.crc32(ihdr) & 0xFFFFFFFF != stored_crc:
        fail("entry.png has a bad IHDR checksum")
    if data[-12:] != struct.pack(">I", 0) + b"IEND" + struct.pack(
            ">I", binascii.crc32(b"IEND") & 0xFFFFFFFF):
        fail("entry.png does not end with a whole IEND chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        fail("entry.png is %dx%d, over the 1024x1024 limit"
             % (width, height))
    return width, height


def main():
    if not os.path.isfile(SOURCE):
        fail("entry.png is missing next to main.py")
    with open(SOURCE, "rb") as handle:
        data = handle.read()
    width, height = check_png(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(data)
    print("wrote %s (%dx%d, %d bytes)" % (target, width, height,
                                          len(data)))


if __name__ == "__main__":
    main()
