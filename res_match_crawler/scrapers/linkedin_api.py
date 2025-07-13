"""Scraper implementation that uses LinkedIn Jobs API via RapidAPI.

This scraper requires an environment variable LINKEDIN_API_KEY to be set with your RapidAPI key.
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
    """Fetch job postings via LinkedIn Jobs API on RapidAPI."""

    name: str = "LinkedInAPI"
    API_ENDPOINT: str = "https://linkedin-jobs-search.p.rapidapi.com/search"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("LINKEDIN_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "LinkedInAPIScraper requires LINKEDIN_API_KEY environment variable or api_key arg"
            )
        self._session = requests.Session()
        self._session.headers.update(
            {
                "x-rapidapi-key": self.api_key,
                "x-rapidapi-host": "linkedin-jobs-search.p.rapidapi.com",
            }
        )

    def search(
        self,
        keyword: str,
        location: str = "",
        *,
        limit: int = 20,
    ) -> List[JobPosting]:
        params: dict[str, str] = {
            "keywords": keyword,  # RapidAPI uses 'keywords' not 'keyword'
            "location": location,
            "limit": str(limit),
        }
        logger.info("LinkedIn API search: %s", params)

        try:
            response = self._session.get(self.API_ENDPOINT, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            logger.debug(
                "API response keys: %s",
                list(data.keys()) if isinstance(data, dict) else type(data),
            )

            # RapidAPI LinkedIn Jobs typically returns data in 'data' or 'jobs' field
            jobs_data = data.get("data", data.get("jobs", []))
            if not jobs_data and isinstance(data, list):
                jobs_data = data

            postings: list[JobPosting] = []
            for item in jobs_data:
                if len(postings) >= limit:
                    break

                # Common field mappings for LinkedIn Jobs API
                title = item.get("title") or item.get("job_title") or ""
                company = item.get("company") or item.get("company_name") or ""
                location_text = (
                    item.get("location") or item.get("job_location") or location
                )
                description = (
                    item.get("description") or item.get("job_description") or ""
                )
                url = item.get("url") or item.get("job_url") or item.get("link") or ""

                postings.append(
                    JobPosting(
                        title=title,
                        description=description,
                        location=location_text,
                        company=company,
                        url=url,
                    )
                )

            logger.info("Successfully parsed %d job postings", len(postings))
            return postings

        except requests.exceptions.RequestException as e:
            logger.error("API request failed: %s", e)
            raise
        except Exception as e:
            logger.error("Failed to parse API response: %s", e)
            raise
