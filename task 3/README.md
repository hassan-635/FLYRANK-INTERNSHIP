# Task 3 — Ethical Web Scraper 🕷️

> **FlyRank Internship | Week 5**
> Build a scraper that collects pages from a practice site, extracts and cleans useful fields, and saves structured records — while behaving like a bot the site's owner would allow.

## 🎯 What This Does

Scrapes **[Books to Scrape](https://books.toscrape.com/)** (a purpose-built practice site) and extracts **1000 book records** with the following fields:

| Field | Type | Example |
|---|---|---|
| `title` | string | `"A Light in the Attic"` |
| `category` | string | `"Poetry"` |
| `price_gbp` | float | `51.77` |
| `rating` | int (1-5) | `3` |
| `stock_count` | int | `22` |
| `description` | string | Cleaned book description |
| `upc` | string | `"a897fe39b1053632"` |
| `price_excl_tax` | float | `51.77` |
| `price_incl_tax` | float | `51.77` |
| `tax` | float | `0.00` |
| `availability` | string | `"In stock (22 available)"` |
| `number_of_reviews` | int | `0` |
| `image_url` | string | Full URL to cover image |
| `url` | string | Source page URL |

## 🏗️ Architecture

```
fetch → parse → extract → clean → structure
```

| Module | Responsibility |
|---|---|
| `config.py` | All tunables (rate limits, URLs, output paths) |
| `fetcher.py` | HTTP layer — robots.txt, rate limiting, retries, User-Agent |
| `parser.py` | BeautifulSoup parsing, field extraction, data cleaning |
| `scraper.py` | Pipeline orchestrator — ties everything together |

## 🤝 Politeness Layer (Professionalism)

| Practice | Implementation |
|---|---|
| **robots.txt** | Checked before crawling — scraper aborts if disallowed |
| **Rate limiting** | 1-second delay between requests (configurable) |
| **User-Agent** | Honest identification: `FlyRank-InternBot/1.0` |
| **Retries** | Exponential backoff on 5xx errors (max 3 retries) |
| **Timeouts** | 15s per request to avoid hanging |
| **Logging** | Full transparency on what the scraper does |

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test run (2 pages ≈ 40 books, ~1 min)
python scraper.py --max-pages 2

# 3. Full run (all 1000 books, ~20 min with rate limiting)
python scraper.py
```

## 📂 Output

```
output/
├── books.json        # Structured records (pretty-printed)
├── books.csv         # Tabular format for analysis
└── scrape_log.json   # Run metadata (timing, counts, politeness config)
```

## 📋 Sample Output (JSON)

```json
{
  "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "title": "A Light in the Attic",
  "category": "Poetry",
  "rating": 3,
  "price_gbp": 51.77,
  "stock_count": 22,
  "description": "It's hard to imagine a world without A Light in the Attic...",
  "upc": "a897fe39b1053632",
  "product_type": "Books",
  "price_excl_tax": 51.77,
  "price_incl_tax": 51.77,
  "tax": 0.0,
  "availability": "In stock (22 available)",
  "number_of_reviews": 0,
  "image_url": "https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"
}
```

## 🔧 Configuration

All settings live in `config.py` — no magic numbers in the codebase:

```python
REQUEST_DELAY_SECONDS = 1.0   # Rate limit between requests
MAX_PAGES = None               # None = all pages, int = cap
MAX_RETRIES = 3                # Retries on server errors
REQUEST_TIMEOUT = 15           # Seconds before giving up
```

## 🔮 Next Steps (Week 6 — RAG Corpus)

The `books.json` output is designed to serve as the **corpus for a RAG pipeline**:
- Each record has a rich `description` field for embedding
- Structured metadata (`category`, `rating`, `price`) enables filtered retrieval
- Clean, consistent schema makes ingestion straightforward
