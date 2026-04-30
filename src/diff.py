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
