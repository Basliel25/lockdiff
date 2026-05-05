"""
CLI entry point
Arguments: python -m lockdiff [path to old.lock] [path to new.lock]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .diff import diff
from .parser import Parse
from .render import render

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
            prog = "lockdiff",
            description = "Human-readable diff for uv.lock files")
    p.add_argument("old", type=Path, help="Path to old lockfile.")
    p.add_argument("new", type=Path, help="Path to new lockfile.")

    args=p.parse_args(argv)

    # Check if file exists
    try:
        old_pkgs = Parse(args.old)
        new_pkgs = Parse(args.new)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


