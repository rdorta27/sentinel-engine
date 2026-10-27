"""Tests for the numbers.json copy of the site repository.

The site lives in its own repository, next to this one. These tests read the
copy at `site_numbers.OUT` and compare it with a fresh build. When the checkout
of the site repository is missing, both tests skip with the reason.

Run from the repository root: python3 -m pytest scripts/test_site_numbers.py -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import site_numbers as sn  # noqa: E402

HAS_COPY = pytest.mark.skipif(
    not sn.OUT.exists(),
    reason=f"no numbers.json at {sn.OUT}; clone sentinel-engine-site next to this repository",
)


@HAS_COPY
def test_numbers_json_matches_evidence():
    assert sn.OUT.read_text() == sn.render(sn.build()), "run scripts/site_numbers.py"


@HAS_COPY
def test_markdown_number_marks_match_the_evidence():
    assert sn.sync_markdown(json.loads(sn.OUT.read_text())["numbers"], check=True) == []
