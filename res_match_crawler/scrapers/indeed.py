"""Scraper for Indeed job listings."""

from __future__ import annotations

import logging
import urllib.parse as _urlparse
from typing import List

from bs4 import BeautifulSoup

from res_match_crawler.http_helper import get_html
from res_match_crawler.models import JobPosting
from .base import JobBoardScraper

logger = logging.getLogger(__name__)


class IndeedScraper(JobBoardScraper):
    """Fetch and parse job postings from Indeed."""

    name: str = "Indeed"
    BASE_URL: str = "https://www.indeed.com"
    SEARCH_PATH: str = "/jobs"

    def search(
        self,
        keyword: str,
        location: str = "",
        *,
        limit: int = 20,
    ) -> List[JobPosting]:
        """Search Indeed for *keyword* in *location* and return a list of JobPosting.

        Parameters
        ----------
        keyword : str
            Search query, e.g. "python developer".
        location : str, optional
            City, state or country. Empty string for worldwide.
        limit : int, default 20
            Maximum number of job postings to return.
        """
        params: dict[str, str] = {
            "q": keyword,
            "l": location,
            "limit": str(limit),
        }
        search_url = f"{self.BASE_URL}{self.SEARCH_PATH}"
        logger.info("Searching Indeed: %s", params)

        html = get_html(search_url, params=params)
        soup = BeautifulSoup(html, "lxml")

        postings: list[JobPosting] = []
        for card in soup.select("a.tapItem"):
            if len(postings) >= limit:
                break

            try:
                job = self._parse_card(card, location_fallback=location)
                if job:
                    postings.append(job)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to parse job card: %s", exc, exc_info=False)

        return postings

    def _parse_card(self, card, *, location_fallback: str = "") -> JobPosting | None:  # type: ignore[valid-type]
        """Convert a job card element to JobPosting (may fetch detail page)."""
        href = card.get("href")
        if not href:
            return None

        detail_url = _urlparse.urljoin(self.BASE_URL, href)

        title = card.select_one("h2.jobTitle span") or card.select_one("h2.jobTitle")
        company = card.select_one("span.companyName")
        loc_elem = card.select_one("div.companyLocation")

        title_text = title.get_text(strip=True) if title else ""
        company_text = company.get_text(strip=True) if company else ""
        location_text = (
            loc_elem.get_text(strip=True) if loc_elem else location_fallback or ""
        )

        # Fetch full description from detail page
        description = self._fetch_description(detail_url)

        return JobPosting(
            title=title_text,
            description=description,
            location=location_text,
            company=company_text,
            url=detail_url,
        )

    def _fetch_description(self, url: str) -> str:
        """Return full job description text from the job detail page."""
        try:
            html = get_html(url)
        except Exception as exc:  # noqa: BLE001
            logger.debug("Failed to retrieve detail page %s: %s", url, exc)
            return ""

        soup = BeautifulSoup(html, "lxml")
        desc_elem = soup.select_one("div#jobDescriptionText") or soup.select_one(
            "div.jobsearch-jobDescriptionText"
        )
        return desc_elem.get_text(separator="\n").strip() if desc_elem else ""
