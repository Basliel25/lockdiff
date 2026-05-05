"""Promgram test for lockdiff"""

from pathlib import Path

from lockdiff.diff import diff
from lockdiff.Parser import parse
from lockdiff.render import render

TEST_FILES = Path(__file__).parent / "test_data"

def test_identity_diff_is_empty():
    pkgs = parse(TEST_FILES / "old.lock")
    result = diff(pkgs, pkgs)
    assert result.is_empty
    assert render(result) == "No changes."
