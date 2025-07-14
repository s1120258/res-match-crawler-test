"""Scraper implementation for RemoteOK API.

RemoteOK provides a free public API for remote job listings.
No authentication required.
API Documentation: https://remoteok.io/api
"""

from __future__ import annotations

import logging
import time
from typing import List

import requests

from res_match_crawler.models import JobPosting
from .base import JobBoardScraper

logger = logging.getLogger(__name__)


class RemoteOKScraper(JobBoardScraper):
    """Fetch remote job postings from RemoteOK API."""

    name: str = "RemoteOK"
    API_ENDPOINT: str = "https://remoteok.io/api"

    def __init__(self) -> None:
        self._session = requests.Session()
        # RemoteOK requires a User-Agent header
        self._session.headers.update(
            {
                "User-Agent": "res-match-crawler/1.0 (https://github.com/example/res-match-crawler)"
            }
        )

    def search(
        self,
        keyword: str,
        location: str = "",
        *,
        limit: int = 20,
    ) -> List[JobPosting]:
        """Search RemoteOK for remote jobs.

        Note: RemoteOK API returns all jobs, so we filter by keyword locally.
        The location parameter is ignored since all jobs are remote.
        """
        logger.info("RemoteOK API search for keyword: %s", keyword)

        try:
            # Add a small delay to be respectful to the API
            time.sleep(0.5)

            response = self._session.get(self.API_ENDPOINT, timeout=30)
            response.raise_for_status()
            data = response.json()

            # RemoteOK API returns a list where the first item is metadata
            # and the rest are job postings
            if not data or len(data) < 2:
                logger.warning("No jobs found in RemoteOK API response")
                return []

            # Skip the first item (metadata) and process job listings
            jobs_data = data[1:]  # Skip metadata
            logger.debug("Found %d total jobs from RemoteOK", len(jobs_data))

            postings: list[JobPosting] = []
            keyword_lower = keyword.lower()

            for job in jobs_data:
                if len(postings) >= limit:
                    break

                # Filter by keyword in title, description, or tags
                title = job.get("position", "")
                description = job.get("description", "")
                tags = " ".join(job.get("tags", []))

                # Check if keyword matches
                search_text = f"{title} {description} {tags}".lower()
                if keyword_lower not in search_text:
                    continue

                # Extract job information
                company = job.get("company", "")
                url = job.get("url", "")
                if url and not url.startswith("http"):
                    url = f"https://remoteok.io/remote-jobs/{job.get('id', '')}"

                # RemoteOK jobs are all remote by definition
                location_text = "Remote"
                if job.get("location"):
                    location_text = f"Remote ({job.get('location')})"

                postings.append(
                    JobPosting(
                        title=title,
                        description=description,
                        location=location_text,
                        company=company,
                        url=url,
                    )
                )

            logger.info("Successfully filtered %d matching job postings", len(postings))
            return postings

        except requests.exceptions.RequestException as e:
            logger.error("RemoteOK API request failed: %s", e)
            raise
        except Exception as e:
            logger.error("Failed to parse RemoteOK API response: %s", e)
            raise
