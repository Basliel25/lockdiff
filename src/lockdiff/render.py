"""
Render a DiffResult as human-readable text.
"""
from __future__ import annotations

import os
import sys

from .diff import DiffResult


RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"
GREEN = "\x1b[32m"
RED = "\x1b[31m"
YELLOW = "\x1b[33m"
CYAN = "\x1b[36m"
MAGENTA = "\x1b[35m"
GREY = "\x1b[90m"


def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return sys.stdout.isatty()


def _styler(enabled: bool):
    if enabled:
        return lambda s, c: f"{c}{s}{RESET}"
    return lambda s, c: s


def _tag(is_direct: bool, c) -> str:
    return "" if is_direct else c(" (transitive)", GREY)


def _box(title: str, count: int, color: str, c) -> str:
    label = f" {title} ({count}) "
    bar = "─" * (len(label) + 2)
    top = c(f"┌{bar}┐", color)
    mid = c(f"│ {BOLD}{label}{RESET}{color} │", color) if color else f"│ {label} │"
    bot = c(f"└{bar}┘", color)
    return f"{top}\n{mid}\n{bot}"


def render(result: DiffResult) -> str:
    use_color = _supports_color()
    c = _styler(use_color)

    if result.is_empty:
        return c("✓ No changes.", GREEN + BOLD)

    name_width = 0
    for pkg in result.added + result.removed:
        name_width = max(name_width, len(pkg.name))
    for b in result.bumped:
        name_width = max(name_width, len(b.name))

    sections: list[str] = []

    if result.added:
        lines = [_box("Added", len(result.added), GREEN, c)]
        for pkg in result.added:
            sym = c("+", GREEN + BOLD)
            name = c(pkg.name.ljust(name_width), GREEN)
            ver = c(pkg.version, BOLD)
            lines.append(f"  {sym} {name}  {ver}{_tag(pkg.is_direct, c)}")
        sections.append("\n".join(lines))

    if result.removed:
        lines = [_box("Removed", len(result.removed), RED, c)]
        for pkg in result.removed:
            sym = c("-", RED + BOLD)
            name = c(pkg.name.ljust(name_width), RED)
            ver = c(pkg.version, BOLD)
            lines.append(f"  {sym} {name}  {ver}{_tag(pkg.is_direct, c)}")
        sections.append("\n".join(lines))

    if result.bumped:
        old_w = max((len(b.old_version) for b in result.bumped), default=0)
        lines = [_box("Bumped", len(result.bumped), YELLOW, c)]
        for b in result.bumped:
            sym = c("~", YELLOW + BOLD)
            name = c(b.name.ljust(name_width), CYAN)
            old_v = c(b.old_version.rjust(old_w), DIM)
            arrow = c("→", YELLOW)
            new_v = c(b.new_version, BOLD + GREEN)
            lines.append(
                f"  {sym} {name}  {old_v} {arrow} {new_v}{_tag(b.is_direct, c)}"
            )
        sections.append("\n".join(lines))

    summary_parts = []
    if result.added:
        summary_parts.append(c(f"+{len(result.added)} added", GREEN))
    if result.removed:
        summary_parts.append(c(f"-{len(result.removed)} removed", RED))
    if result.bumped:
        summary_parts.append(c(f"~{len(result.bumped)} bumped", YELLOW))
    summary = c("Summary: ", BOLD) + c(" · ", GREY).join(summary_parts)
    sections.append(summary)

    return "\n\n".join(sections)
