"""Command-line interface for res_match_crawler.

Example:
    python -m res_match_crawler.cli "python developer" -l "New York, NY" -n 10 --json
"""

from __future__ import annotations

import argparse
import json
import logging
from typing import List

from res_match_crawler.models import JobPosting
from res_match_crawler.scrapers import IndeedScraper


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch job postings from Indeed based on keyword and location.",
    )
    parser.add_argument("keyword", help="Search keyword, e.g. 'python developer'")
    parser.add_argument(
        "-l",
        "--location",
        default="",
        help="Location filter, e.g. 'New York, NY'. Leave blank for worldwide.",
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=20,
        help="Maximum number of job postings to retrieve (default: 20)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of plain text.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity level (-v, -vv).",
    )
    return parser.parse_args()


def _configure_logging(verbosity: int) -> None:
    """Configure root logger based on *verbosity* flag."""
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def main() -> None:  # noqa: D401
    """Entry point for the CLI."""
    args = _parse_args()
    _configure_logging(args.verbose)

    scraper = IndeedScraper()
    jobs: List[JobPosting] = scraper.search(
        args.keyword, args.location, limit=args.limit
    )

    if args.json:
        print(json.dumps([job.to_dict() for job in jobs], ensure_ascii=False, indent=2))
    else:
        for job in jobs:
            print(job)


if __name__ == "__main__":  # pragma: no cover
    main()
