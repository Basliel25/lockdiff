"""Detect lockfile ecosystem from file contents."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

Ecosystem = Literal["uv", "npm"]


def detect_format(path: Path) -> Ecosystem:
    """Return "npm" if the file looks like JSON, else "uv" (TOML).

    Sniffs the first non-whitespace byte: `{` → npm package-lock.json,
    anything else → uv.lock (TOML).
    """
    with path.open("rb") as f:
        chunk = f.read(512)

    for byte in chunk:
        if byte in (0x20, 0x09, 0x0A, 0x0D):  # space, tab, LF, CR
            continue
        return "npm" if byte == 0x7B else "uv"  # '{'

    raise ValueError(f"{path}: file is empty or whitespace-only")
