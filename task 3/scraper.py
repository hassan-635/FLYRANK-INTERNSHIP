"""
scraper.py — Main orchestrator
================================
Pipeline:  CHECK ROBOTS → FETCH listings → EXTRACT book URLs → FETCH details
           → PARSE & CLEAN → SAVE structured output

Usage:
    python scraper.py              # scrape all 1000 books
    python scraper.py --max-pages 2   # quick test run (first 2 pages ≈ 40 books)
"""

# Fix Windows console encoding (cp1252 → UTF-8) so emoji/Unicode prints correctly
import sys
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

import argparse
import csv
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone

from config import (
    BASE_URL,
    CATALOGUE_URL,
    MAX_PAGES,
    OUTPUT_CSV,
    OUTPUT_DIR,
    OUTPUT_JSON,
    SCRAPE_LOG,
    USER_AGENT,
)
from fetcher import check_robots_txt, create_session, fetch_page
from parser import parse_book_detail, parse_listing_page

# ─── Logging Setup ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# Pipeline Steps
# ═══════════════════════════════════════════════════════════════

def collect_book_urls(session, max_pages: int | None) -> list[str]:
    """
    Step 1 — Walk through all listing pages and gather book detail URLs.
    """
    all_urls: list[str] = []
    page_url = f"{CATALOGUE_URL}page-1.html"
    page_num = 0

    while page_url:
        page_num += 1
        if max_pages and page_num > max_pages:
            logger.info("🛑 Reached max-pages limit (%d)", max_pages)
            break

        html = fetch_page(session, page_url)
        if html is None:
            logger.error("⚠️  Failed to fetch listing page %d — stopping pagination", page_num)
            break

        book_urls, next_page = parse_listing_page(html, page_url)
        all_urls.extend(book_urls)
        page_url = next_page

        logger.info("📚 Page %d done — %d total book URLs collected so far", page_num, len(all_urls))

    return all_urls


def scrape_books(session, book_urls: list[str]) -> list[dict]:
    """
    Step 2 — Fetch each book detail page and extract structured records.
    """
    records: list[dict] = []
    total = len(book_urls)

    for idx, url in enumerate(book_urls, start=1):
        html = fetch_page(session, url)
        if html is None:
            logger.warning("⚠️  Skipping book %d/%d (fetch failed): %s", idx, total, url)
            continue

        record = parse_book_detail(html, url)
        records.append(record)

        if idx % 50 == 0 or idx == total:
            logger.info("📖 Scraped %d / %d books", idx, total)

    return records


# ═══════════════════════════════════════════════════════════════
# Output Writers
# ═══════════════════════════════════════════════════════════════

def save_json(records: list[dict], filepath: str) -> None:
    """Write records to a pretty-printed JSON file."""
    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(records, fh, indent=2, ensure_ascii=False)
    logger.info("💾 Saved %d records → %s", len(records), filepath)


def save_csv(records: list[dict], filepath: str) -> None:
    """Write records to a CSV file with all fields as columns."""
    if not records:
        logger.warning("⚠️  No records to save as CSV")
        return

    # Collect ALL keys across every record (some books may lack certain fields)
    fieldnames: list[str] = []
    seen: set[str] = set()
    for rec in records:
        for key in rec:
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)

    with open(filepath, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    logger.info("💾 Saved %d records → %s", len(records), filepath)


def save_scrape_log(meta: dict, filepath: str) -> None:
    """Save metadata about this scrape run."""
    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
    logger.info("📝 Scrape log → %s", filepath)


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(description="Ethical scraper for books.toscrape.com")
    parser.add_argument(
        "--max-pages",
        type=int,
        default=MAX_PAGES,
        help="Limit number of listing pages to scrape (default: all)",
    )
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  📚  FlyRank Internship — Task 3: Ethical Web Scraper")
    print("  🌐  Target: books.toscrape.com")
    print(f"  🤖  User-Agent: {USER_AGENT}")
    print("=" * 60)
    print()

    start_time = time.time()
    started_at = datetime.now(timezone.utc).isoformat()

    # ── Step 0: robots.txt check ──
    logger.info("🔍 Step 0 — Checking robots.txt …")
    if not check_robots_txt(BASE_URL, USER_AGENT):
        logger.error("🚫 Crawling disallowed by robots.txt — aborting.")
        sys.exit(1)

    # ── Step 1: Collect all book URLs ──
    logger.info("🔍 Step 1 — Collecting book URLs from listing pages …")
    session = create_session()
    book_urls = collect_book_urls(session, args.max_pages)
    logger.info("✅ Collected %d book URLs", len(book_urls))

    if not book_urls:
        logger.error("❌ No book URLs found — aborting.")
        sys.exit(1)

    # ── Step 2: Scrape each book detail page ──
    logger.info("🔍 Step 2 — Scraping book detail pages …")
    records = scrape_books(session, book_urls)
    logger.info("✅ Scraped %d books successfully", len(records))

    # ── Step 3: Save structured output ──
    logger.info("🔍 Step 3 — Saving structured output …")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    json_path = os.path.join(OUTPUT_DIR, OUTPUT_JSON)
    csv_path = os.path.join(OUTPUT_DIR, OUTPUT_CSV)
    log_path = os.path.join(OUTPUT_DIR, SCRAPE_LOG)

    save_json(records, json_path)
    save_csv(records, csv_path)

    elapsed = time.time() - start_time

    # ── Scrape metadata log ──
    scrape_meta = {
        "scraper": "FlyRank-InternBot/1.0",
        "target_site": BASE_URL,
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(elapsed, 2),
        "pages_crawled": args.max_pages or "all",
        "books_found": len(book_urls),
        "books_scraped": len(records),
        "books_failed": len(book_urls) - len(records),
        "output_files": {
            "json": json_path,
            "csv": csv_path,
        },
        "politeness": {
            "robots_txt_checked": True,
            "user_agent": USER_AGENT,
            "rate_limit_seconds": 1.0,
            "retries_on_5xx": 3,
        },
    }
    save_scrape_log(scrape_meta, log_path)

    # ── Summary ──
    print()
    print("=" * 60)
    print(f"  ✅  DONE — {len(records)} books scraped in {elapsed:.1f}s")
    print(f"  📁  JSON → {json_path}")
    print(f"  📁  CSV  → {csv_path}")
    print(f"  📁  Log  → {log_path}")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
