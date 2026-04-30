"""
This program parses a uv.lock file into a list of package objeects listed in the file.

@author: Basliel B. Gugsa
@last_edit:30/04/26
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Package:
    """A single package entry from a lockfile.

    `is_direct` is True if listed in the root project's
    dependencies.

    `dependencies` :a tuple of names 
    """
    name: str
    version: str
    is_direct: bool = False
    dependencies: tuple[str, ...] = field(default_factory=tuple)


def parse(path: Path) -> dict[str, Package]:
    """Parse a uv.lock file at `path`. Return {name: Package}.

    The root project is filtered out of the result.
    """
    with path.open("rb") as f:
        data = tomllib.load(f)

    raw_packages = data.get("package", [])
    if not raw_packages:
        raise ValueError(f"{path}: no [[package]] entries, not a uv.lock?")

    direct_deps: set[str] = set()

    for pkg in raw_packages:
        ...

    result: dict[str, Package] = {}

    for pkg in raw_packages:
        ...

    return result
