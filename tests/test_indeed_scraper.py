"""Unit tests for IndeedScraper.

Network calls are stubbed via monkeypatch so tests run offline.
"""

from __future__ import annotations

import pytest
from unittest.mock import Mock

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


def test_search_parses_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """scraper.search should parse two job postings correctly."""

    def mock_session_get(url, **kwargs):
        """Mock requests.Session.get method."""
        response = Mock()
        response.status_code = 200
        response.raise_for_status.return_value = None

        if "/jobs" in url:
            response.text = SEARCH_HTML
        else:
            response.text = DETAIL_HTML

        return response

    # Mock the session's get method directly
    monkeypatch.setattr(http_helper._SESSION, "get", mock_session_get)

    scraper = IndeedScraper()
    jobs = scraper.search("python", limit=2)

    assert len(jobs) == 2

    first = jobs[0]
    assert first.title == "Python Developer"
    assert first.company == "Acme Corp"
    assert first.location == "Remote"
    assert "Python position" in first.description
    assert first.url == "https://www.indeed.com/rc/clk?jk=123"
