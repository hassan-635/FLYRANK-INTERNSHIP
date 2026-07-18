"""
parser.py — HTML parsing & data extraction
============================================
Handles:
  • Listing-page parsing (book URLs + pagination)
  • Detail-page parsing (all product fields)
  • Data cleaning (prices → floats, ratings → ints, availability → int)
"""

import re
import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from config import BASE_URL, CATALOGUE_URL, STAR_RATING_MAP

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# Listing-page helpers
# ═══════════════════════════════════════════════════════════════

def parse_listing_page(html: str, current_url: str) -> tuple[list[str], str | None]:
    """
    Parse a catalogue listing page.

    Returns
    -------
    book_urls : list[str]
        Absolute URLs of individual book detail pages.
    next_page_url : str | None
        Absolute URL of the next listing page, or None if this is the last page.
    """
    soup = BeautifulSoup(html, "lxml")

    # ── Extract book detail URLs ──
    book_urls: list[str] = []
    for article in soup.select("article.product_pod"):
        link_tag = article.select_one("h3 > a")
        if link_tag and link_tag.get("href"):
            href = link_tag["href"]
            # Listing pages use relative paths like '../book-name_123/index.html'
            absolute = urljoin(current_url, href)
            book_urls.append(absolute)

    # ── Extract "next page" link ──
    next_page_url = None
    next_btn = soup.select_one("li.next > a")
    if next_btn and next_btn.get("href"):
        next_page_url = urljoin(current_url, next_btn["href"])

    logger.info("📄 Found %d books on page, next=%s", len(book_urls), next_page_url)
    return book_urls, next_page_url


# ═══════════════════════════════════════════════════════════════
# Detail-page parser
# ═══════════════════════════════════════════════════════════════

def parse_book_detail(html: str, url: str) -> dict:
    """
    Extract and clean all useful fields from a single book's detail page.

    Returns a flat dict ready for JSON/CSV serialization.
    """
    soup = BeautifulSoup(html, "lxml")
    record: dict = {"url": url}

    # ── Title ──
    h1 = soup.select_one("article.product_page h1")
    record["title"] = h1.get_text(strip=True) if h1 else ""

    # ── Category (from breadcrumb) ──
    breadcrumbs = soup.select("ul.breadcrumb li")
    if len(breadcrumbs) >= 3:
        # Home > Books > Category > Title
        record["category"] = breadcrumbs[-2].get_text(strip=True)
    else:
        record["category"] = ""

    # ── Star Rating ──
    star_tag = soup.select_one("p.star-rating")
    if star_tag:
        classes = star_tag.get("class", [])
        for cls in classes:
            if cls in STAR_RATING_MAP:
                record["rating"] = STAR_RATING_MAP[cls]
                break
        else:
            record["rating"] = None
    else:
        record["rating"] = None

    # ── Price ──
    price_tag = soup.select_one("p.price_color")
    record["price_gbp"] = _clean_price(price_tag.get_text(strip=True)) if price_tag else None

    # ── Availability ──
    avail_tag = soup.select_one("p.instock.availability")
    if avail_tag:
        avail_text = avail_tag.get_text(strip=True)
        record["availability"] = avail_text
        record["stock_count"] = _extract_stock_count(avail_text)
    else:
        record["availability"] = ""
        record["stock_count"] = 0

    # ── Product Description ──
    desc_header = soup.select_one("#product_description")
    if desc_header:
        desc_p = desc_header.find_next_sibling("p")
        record["description"] = _clean_description(desc_p.get_text(strip=True)) if desc_p else ""
    else:
        record["description"] = ""

    # ── Product Information Table ──
    info_table = soup.select_one("table.table-striped")
    if info_table:
        for row in info_table.select("tr"):
            th = row.select_one("th")
            td = row.select_one("td")
            if th and td:
                key = _normalize_key(th.get_text(strip=True))
                value = td.get_text(strip=True)
                record[key] = value

    # ── Clean up price fields from the table ──
    for price_key in ("price_excl_tax", "price_incl_tax", "tax"):
        if price_key in record:
            record[price_key] = _clean_price(record[price_key])

    # ── Clean number_of_reviews → int ──
    if "number_of_reviews" in record:
        try:
            record["number_of_reviews"] = int(record["number_of_reviews"])
        except (ValueError, TypeError):
            record["number_of_reviews"] = 0

    # ── Image URL ──
    img_tag = soup.select_one("#product_gallery img")
    if img_tag and img_tag.get("src"):
        record["image_url"] = urljoin(url, img_tag["src"])
    else:
        record["image_url"] = ""

    return record


# ═══════════════════════════════════════════════════════════════
# Cleaning helpers
# ═══════════════════════════════════════════════════════════════

def _clean_price(raw: str) -> float | None:
    """'£51.77' or 'Â£51.77' → 51.77"""
    match = re.search(r"[\d]+\.[\d]{2}", raw)
    if match:
        return float(match.group())
    return None


def _extract_stock_count(text: str) -> int:
    """'In stock (22 available)' → 22"""
    match = re.search(r"\((\d+)\s+available\)", text)
    return int(match.group(1)) if match else 0


def _clean_description(text: str) -> str:
    """Strip trailing '...more' artifacts and excessive whitespace."""
    text = re.sub(r"\s*\.{3}more\s*$", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _normalize_key(raw: str) -> str:
    """
    'Price (excl. tax)' → 'price_excl_tax'
    'Number of reviews' → 'number_of_reviews'
    """
    key = raw.lower()
    key = re.sub(r"[().]", "", key)
    key = re.sub(r"\s+", "_", key.strip())
    return key
