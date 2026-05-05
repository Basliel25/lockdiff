"""
Computes the diff between two parsed lockfiles.

@author: Basliel B. Gugsa
@last_edit:30/04/26
"""
from __future__ import annotations

from dataclasses import dataclass

from .Parser import Package


@dataclass(frozen=True)
class Bump:
    name: str
    old_version: str
    new_version: str
    is_direct: bool


@dataclass(frozen=True)
class DiffResult:
    added: list[Package]
    removed: list[Package]
    bumped: list[Bump]

    @property
    def is_empty(self) -> bool:
        return not (self.added or self.removed or self.bumped)

def diff(old: dict[str, Package], new: dict[str, Package]) -> DiffResult:
    """Compare two parsed lockfiles. Result is sorted alphabetically per category."""
    old_names = set(old)
    new_names = set(new)

    added = sorted(
        (new[name] for name in new_names - old_names),
        key=lambda p: p.name,
    )
    removed = sorted(
        (old[name] for name in old_names - new_names),
        key=lambda p: p.name,
    )

    # List of bumped packages
    bumped: list[Bump] = []
    for name in sorted(old_names & new_names):
        if old[name].version != new[name].version:
            bumped.append(
                Bump(
                    name=name,
                    old_version=old[name].version,
                    new_version=new[name].version,

                    # Using new's direct status
                    is_direct=new[name].is_direct,
                )
            )

    return DiffResult(added=added, removed=removed, bumped=bumped)
    
