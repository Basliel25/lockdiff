"""
CLI entry point
Arguments: python -m lockdiff [path to old.lock] [path to new.lock]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .diff import diff
from .Parser import parse
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
        old_pkgs = parse(args.old)
        new_pkgs = parse(args.new)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    result = diff(old_pkgs, new_pkgs)
    print(render(result))

    return 0 if result.is_empty else 1

if __name__ == "__main__":
    raise SystemExit(main())


