"""Scraper implementations for various job boards."""

from __future__ import annotations

from .base import JobBoardScraper
from .indeed import IndeedScraper

__all__: list[str] = [
    "JobBoardScraper",
    "IndeedScraper",
]