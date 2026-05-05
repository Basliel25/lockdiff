"""
Parse a package-lock.json (npm) file into a {(name, version): Package} dict.

@author: Basliel B. Gugsa
"""
from __future__ import annotations

import json
from pathlib import Path

from .Parser import Package


def parse_npm(path: Path) -> dict[tuple[str, str], Package]:
    """Parse package-lock.json. Return {(name, version): Package}.
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

    result: dict[tuple[str, str], Package] = {}

    for install_path, entry in packages.items():
        if install_path == "":
            continue  # skiping root

        name = _name_from_path(install_path)
        if name is None:
            continue  # workspace entries are ignored

        pkg_version = entry.get("version")
        if pkg_version is None:
            continue

        key = (name, pkg_version)
        # Ignore dublicate install of same package
        if key in result:
            continue

        result[key] = Package(
            name=name,
            version=pkg_version,
            is_direct=name in direct_names,
        )

    if not result:
        raise ValueError(f"{path}: parsed 0 packages, file is empty")

    return result


def _name_from_path(install_path: str) -> str | None:
    """Extract package name from an npm install path.
    """
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
