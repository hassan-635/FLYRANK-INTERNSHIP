"""
Configuration for the Books to Scrape web scraper.
All tunables live here — no magic numbers in the scraper itself.
"""

# ─── Target Site ─────────────────────────────────────────────
BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = f"{BASE_URL}catalogue/"

# ─── Polite Crawling ────────────────────────────────────────
# Seconds to wait between consecutive HTTP requests (rate limit)
REQUEST_DELAY_SECONDS = 1.0

# Identify ourselves honestly in every request
USER_AGENT = "FlyRank-InternBot/1.0 (hassan-635; educational-scraper; +https://github.com/hassan-635)"

# Maximum retries for transient failures (5xx, timeouts)
MAX_RETRIES = 3

# Timeout for each HTTP request (seconds)
REQUEST_TIMEOUT = 15

# ─── Scrape Scope ────────────────────────────────────────────
# Set to None to scrape ALL pages; set to an int to cap (useful for dev/testing)
MAX_PAGES = None

# ─── Output ──────────────────────────────────────────────────
OUTPUT_DIR = "output"
OUTPUT_JSON = "books.json"
OUTPUT_CSV = "books.csv"
SCRAPE_LOG = "scrape_log.json"

# ─── Star-Rating Mapping ────────────────────────────────────
STAR_RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}
