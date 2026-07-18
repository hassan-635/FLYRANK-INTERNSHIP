"""
fetcher.py — Responsible HTTP layer
====================================
Handles:
  • robots.txt compliance check
  • Rate-limited, retried GET requests
  • Honest User-Agent identification
"""

import time
import logging
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import (
    BASE_URL,
    REQUEST_DELAY_SECONDS,
    USER_AGENT,
    MAX_RETRIES,
    REQUEST_TIMEOUT,
)

logger = logging.getLogger(__name__)


# ─── robots.txt Compliance ──────────────────────────────────
def check_robots_txt(base_url: str, user_agent: str) -> bool:
    """
    Parse robots.txt and verify we are allowed to crawl.
    Returns True if crawling is permitted (or if no robots.txt exists).
    """
    robots_url = urljoin(base_url, "/robots.txt")
    rp = RobotFileParser()
    rp.set_url(robots_url)

    try:
        rp.read()
        allowed = rp.can_fetch(user_agent, base_url)
        if allowed:
            logger.info("✅ robots.txt permits crawling for '%s'", user_agent)
        else:
            logger.warning("🚫 robots.txt DISALLOWS crawling for '%s'", user_agent)
        return allowed
    except Exception as exc:
        # No robots.txt → default to allowed (common convention)
        logger.info(
            "ℹ️  No robots.txt found at %s (%s) — proceeding with crawl",
            robots_url,
            exc,
        )
        return True


# ─── Session Factory ────────────────────────────────────────
def create_session() -> requests.Session:
    """
    Build a requests.Session pre-configured with:
      - Custom User-Agent header
      - Automatic retries on 5xx / connection errors
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )

    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=1,  # 1s, 2s, 4s …
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


# ─── Rate-Limited Fetch ─────────────────────────────────────
_last_request_time: float = 0.0


def fetch_page(session: requests.Session, url: str) -> str | None:
    """
    GET *url* with rate limiting and error handling.
    Returns the page HTML as a string, or None on failure.
    """
    global _last_request_time

    # Enforce minimum delay between requests
    elapsed = time.time() - _last_request_time
    if elapsed < REQUEST_DELAY_SECONDS:
        sleep_for = REQUEST_DELAY_SECONDS - elapsed
        logger.debug("⏳ Rate-limiting: sleeping %.2fs", sleep_for)
        time.sleep(sleep_for)

    try:
        logger.info("🔗 Fetching: %s", url)
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        _last_request_time = time.time()
        response.raise_for_status()
        return response.text

    except requests.exceptions.HTTPError as exc:
        logger.error("❌ HTTP error for %s: %s", url, exc)
    except requests.exceptions.ConnectionError as exc:
        logger.error("❌ Connection error for %s: %s", url, exc)
    except requests.exceptions.Timeout as exc:
        logger.error("❌ Timeout for %s: %s", url, exc)
    except requests.exceptions.RequestException as exc:
        logger.error("❌ Request failed for %s: %s", url, exc)

    return None
