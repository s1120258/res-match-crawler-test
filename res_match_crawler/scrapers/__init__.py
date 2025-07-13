"""Scraper implementations for various job boards."""

from __future__ import annotations

from .indeed import IndeedScraper

__all__: list[str] = [
    "IndeedScraper",
]