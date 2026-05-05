"""
CLI entry point
Arguments: python -m lockdiff [path to old.lock] [path to new.lock]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .detect import detect_format
from .diff import diff
from .Parser import parse
from .Parser_npm import parse_npm
from .render import render

_PARSERS = {"uv": parse, "npm": parse_npm}

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
            prog = "lockdiff",
            description = "Human-readable diff for uv.lock and package-lock.json files")
    p.add_argument("old_lock", type=Path, help="Path to old lockfile.")
    p.add_argument("new_lock", type=Path, help="Path to new lockfile.")

    args=p.parse_args(argv)

    try:
        old_fmt = detect_format(args.old_lock)
        new_fmt = detect_format(args.new_lock)
        if old_fmt != new_fmt:
            print(
                f"error: format mismatch: {args.old_lock} is {old_fmt}, "
                f"{args.new_lock} is {new_fmt}",
                file=sys.stderr,
            )
            return 2
        old_pkgs = _PARSERS[old_fmt](args.old_lock)
        new_pkgs = _PARSERS[new_fmt](args.new_lock)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    result = diff(old_pkgs, new_pkgs)
    print(render(result))

    return 0 if result.is_empty else 1

if __name__ == "__main__":
    raise SystemExit(main())


