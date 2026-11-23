"""Entry for the make.fun bounty "Sum up 22 November's world news in one image".

The grader runs this in a fresh container: a read-only /bot holding this
repository at the submitted commit, a writable /output, no network, 60 seconds.
The program's whole job is to place the day's summary image at /output/entry.png.

Outside the grader, point MAKEFUN_OUTPUT_DIR somewhere writable to try it:

    MAKEFUN_OUTPUT_DIR=out python main.py
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SOURCE = REPO_ROOT / "entry.png"

MAX_BYTES = 1024 * 1024
GATE_SIZE = (1024, 1024)
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def png_dimensions(header: bytes) -> tuple[int, int]:
    """Width and height from a PNG's IHDR chunk, which always starts at byte 16."""
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not SOURCE.is_file():
        fail(f"entry.png is not beside main.py (looked in {SOURCE})")

    size = SOURCE.stat().st_size
    if size == 0:
        fail("entry.png is empty")
    if size > MAX_BYTES:
        fail(f"entry.png is {size} bytes, over the {MAX_BYTES} byte cap")

    with SOURCE.open("rb") as handle:
        header = handle.read(24)
    if header[: len(PNG_MAGIC)] != PNG_MAGIC:
        fail("entry.png does not start with the PNG signature")

    width, height = png_dimensions(header)
    if (width, height) != GATE_SIZE:
        fail(f"entry.png is {width}x{height}, the gate takes {GATE_SIZE[0]}x{GATE_SIZE[1]}")

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")).expanduser()
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        fail(f"cannot create {output_dir}: {exc}")
    if not output_dir.is_dir():
        fail(f"{output_dir} exists but is not a directory")

    target = output_dir / "entry.png"
    shutil.copyfile(SOURCE, target)

    if target.stat().st_size != size:
        fail("the copy is a different size than entry.png")
    if sha256_of(target) != sha256_of(SOURCE):
        fail("the copy does not hash to entry.png")

    print(f"wrote {target} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
