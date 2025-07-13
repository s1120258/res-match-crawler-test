"""Unit tests for IndeedScraper.

Network calls are stubbed via monkeypatch so tests run offline.
"""

from __future__ import annotations

import re

import pytest

from res_match_crawler import http_helper
from res_match_crawler.scrapers import IndeedScraper

SEARCH_HTML = """
<html><body>
<a class="tapItem" href="/rc/clk?jk=123">
  <h2 class="jobTitle"><span>Python Developer</span></h2>
  <span class="companyName">Acme Corp</span>
  <div class="companyLocation">Remote</div>
</a>
<a class="tapItem" href="/rc/clk?jk=456">
  <h2 class="jobTitle"><span>Backend Engineer</span></h2>
  <span class="companyName">Beta Inc</span>
  <div class="companyLocation">New York, NY</div>
</a>
</body></html>
"""

DETAIL_HTML = """
<html><body>
<div id="jobDescriptionText">
<p>Great Python position building APIs.</p>
</div>
</body></html>
"""


def fake_get_html(url: str, *args, **kwargs):  # noqa: D401
    """Return canned HTML depending on *url*."""
    if "/jobs" in url:
        return SEARCH_HTML
    return DETAIL_HTML


def test_search_parses_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """scraper.search should parse two job postings correctly."""
    monkeypatch.setattr(http_helper, "get_html", fake_get_html)

    scraper = IndeedScraper()
    jobs = scraper.search("python", limit=2)

    assert len(jobs) == 2

    first = jobs[0]
    assert first.title == "Python Developer"
    assert first.company == "Acme Corp"
    assert first.location == "Remote"
    assert re.search("Python position", first.description)