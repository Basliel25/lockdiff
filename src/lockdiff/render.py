"""
Render a DiffResult as human-readable text.
"""
from __future__ import annotations

from .diff import DiffResult

def _tag(is_direct: bool) -> str:
    return "" if is_direct else " (transitive)"

def render(result: DiffResult) -> str:
    if result.is_empty:
        return "No changes."

    sections: list[str] = []

    if result.added:
        lines = [f"Added ({len(result.added)}):"]
        for pkg in result.added:
            lines.append(f"  + {pkg.name} {pkg.version}{_tag(pkg.is_direct)}")
        sections.append("\n".join(lines))

    if result.removed:
        lines = [f"Removed ({len(result.removed)}):"]
        for pkg in result.removed:
            lines.append(f"  - {pkg.name} {pkg.version}{_tag(pkg.is_direct)}")
        sections.append("\n".join(lines))

    if result.bumped:
        lines = [f"Bumped ({len(result.bumped)}):"]
        for b in result.bumped:
            lines.append(
                f"  ~ {b.name} {b.old_version} -> {b.new_version}{_tag(b.is_direct)}"
            )
        sections.append("\n".join(lines))

    return "\n\n".join(sections)
