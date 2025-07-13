"""HTTP helper utilities for making robust GET requests.

This module provides a configured `requests.Session` with:
- Default User-Agent identifying the crawler.
- Automatic retries with exponential backoff for transient errors (5xx, connection issues).

Usage:
    from res_match_crawler.http_helper import get_html
    html = get_html("https://example.com", params={"q": "python"})
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry  # type: ignore

logger = logging.getLogger(__name__)

DEFAULT_HEADERS: Dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; ResMatchCrawler/0.1; +https://example.com/bot)"
    )
}


def _create_session(
    retries: int = 3,
    backoff_factor: float = 0.5,
    status_forcelist: tuple[int, ...] = (500, 502, 503, 504),
) -> requests.Session:
    """Return a `requests.Session` pre-configured with retry logic and headers."""

    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=("HEAD", "GET", "OPTIONS"),
        raise_on_status=False,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(DEFAULT_HEADERS)

    return session


# Global session reused across requests to benefit from connection pooling
_SESSION: requests.Session = _create_session()


def get_html(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    timeout: int | float = 10,
    headers: Optional[Dict[str, str]] = None,
) -> str:
    """Fetch the given *url* and return response text.

    Parameters
    ----------
    url : str
        Target URL.
    params : dict, optional
        Query parameters.
    timeout : int | float, default 10
        Request timeout seconds.
    headers : dict, optional
        Extra headers to merge with the defaults.

    Raises
    ------
    requests.HTTPError
        If the final response status is not 2xx.
    """
    hdrs = DEFAULT_HEADERS.copy()
    if headers:
        hdrs.update(headers)

    logger.debug("Fetching URL %s with params=%s", url, params)
    response = _SESSION.get(url, params=params, timeout=timeout, headers=hdrs)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        logger.error("Request failed: %s", e)
        raise

    return response.text
