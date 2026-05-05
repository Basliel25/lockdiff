"""
Parse a package-lock.json (npm) file into a {name: Package} dict.

@author: Basliel B. Gugsa
"""
from __future__ import annotations

import json
from pathlib import Path

from .Parser import Package


def parse_npm(path: Path) -> dict[str, Package]:
    """Parse package-lock.json. Return {name: Package}.

    npm trees may contain multiple versions of the same package. We collapse
    to one entry per name: prefer direct dependencies, then the
    lexicographically highest version string.
    """
    with path.open("rb") as f:
        data = json.load(f)

    version = data.get("lockfileVersion")
    if version not in (2, 3):
        raise ValueError(
            f"{path}: lockfileVersion={version} not supported (need 2 or 3)"
        )

    packages = data.get("packages")
    if not packages:
        raise ValueError(f"{path}: `packages` block not found, not a package-lock.json")

    root = packages.get("", {})
    direct_names: set[str] = set()
    direct_names.update(root.get("dependencies", {}).keys())
    direct_names.update(root.get("devDependencies", {}).keys())
    direct_names.update(root.get("optionalDependencies", {}).keys())

    result: dict[str, Package] = {}

    for install_path, entry in packages.items():
        if install_path == "":
            continue

        name = _name_from_path(install_path)
        if name is None:
            continue

        pkg_version = entry.get("version")
        if pkg_version is None:
            continue

        is_direct = name in direct_names
        candidate = Package(name=name, version=pkg_version, is_direct=is_direct)

        existing = result.get(name)
        if existing is None or _prefer(candidate, existing):
            result[name] = candidate

    if not result:
        raise ValueError(f"{path}: parsed 0 packages, file is empty")

    return result


def _prefer(candidate: Package, existing: Package) -> bool:
    """Return True if `candidate` should replace `existing`.

    Policy: direct beats transitive; otherwise higher version string wins.
    """
    if candidate.is_direct and not existing.is_direct:
        return True
    if existing.is_direct and not candidate.is_direct:
        return False
    return candidate.version > existing.version


def _name_from_path(install_path: str) -> str | None:
    """Extract package name from an npm install path."""
    marker = "node_modules/"
    idx = install_path.rfind(marker)
    if idx == -1:
        return None
    rest = install_path[idx + len(marker):]
    if not rest:
        return None

    if rest.startswith("@"):
        parts = rest.split("/", 2)
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"
        return None

    return rest.split("/", 1)[0]
