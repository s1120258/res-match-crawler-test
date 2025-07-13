"""Scraper implementation that uses a (hypothetical) LinkedIn Jobs REST API.

This scraper requires an environment variable LINKEDIN_API_KEY to be set. The code targets a sample
endpoint `https://api.linkedin-jobs.com/v1/search` (placeholder). You may need to adjust the URL
and field names to match the actual provider you use (e.g. a RapidAPI endpoint).
"""

from __future__ import annotations

import logging
import os
from typing import List

import requests

from res_match_crawler.models import JobPosting
from .base import JobBoardScraper

logger = logging.getLogger(__name__)


class LinkedInAPIScraper(JobBoardScraper):
    """Fetch job postings via LinkedIn Jobs API."""

    name: str = "LinkedInAPI"
    API_ENDPOINT: str = "https://api.linkedin-jobs.com/v1/search"  # placeholder

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("LINKEDIN_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "LinkedInAPIScraper requires LINKEDIN_API_KEY environment variable or api_key arg"
            )
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def search(
        self,
        keyword: str,
        location: str = "",
        *,
        limit: int = 20,
    ) -> List[JobPosting]:
        params: dict[str, str] = {
            "keyword": keyword,
            "location": location,
            "limit": str(limit),
        }
        logger.info("LinkedIn API search: %s", params)
        response = self._session.get(self.API_ENDPOINT, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # The exact JSON structure depends on the API provider. We assume:
        # {
        #   "data": [
        #       {
        #           "title": "...",
        #           "company": "...",
        #           "location": "...",
        #           "description": "...",
        #           "url": "..."
        #       },
        #       ...
        #   ]
        # }
        postings: list[JobPosting] = []
        for item in data.get("data", []):
            postings.append(
                JobPosting(
                    title=item.get("title", ""),
                    description=item.get("description", ""),
                    location=item.get("location", location),
                    company=item.get("company", ""),
                    url=item.get("url", ""),
                )
            )
            if len(postings) >= limit:
                break

        return postings
