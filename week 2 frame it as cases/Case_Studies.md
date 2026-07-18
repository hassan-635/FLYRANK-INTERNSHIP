# Week 2: Frame It as Cases (Work That Speaks for Itself)

**🗣️ Voice Card:** 
> "Direct, technical, plain-spoken, no buzzwords."

---

## 🏗️ Case Study 1: The Polite Web Scraper

**The Problem:** 
Extracting thousands of clean product records from a website without getting IP banned or causing a strain on the target server. Most beginner scripts hammer servers until they crash or get blocked, leaving you with incomplete, messy data.

**What I Did (And Decided):** 
I built a decoupled Python scraping pipeline (`fetcher.py` and `parser.py`). I decided not to use massive frameworks like Scrapy because it was overkill. Instead, I implemented a strict 1-second rate limit, checked `robots.txt` before every crawl, passed an honest custom `User-Agent`, and built an automatic backoff-retry mechanism for 5xx errors. For the UI, I built a vanilla JS/Tailwind dashboard to visualize the JSON output.

**What Came of It:** 
A highly robust scraper that safely pulled 40 books into a RAG-ready structured dataset. The interactive dashboard is deployed live on Vercel, allowing users to filter, sort, and view the scraped data instantly.

---

## 🏗️ Case Study 2: The Background Report Pipeline

**The Problem:** 
A heavy PDF report generation process was blocking API responses. Users had to sit staring at a loading spinner for up to 10 seconds while the server chewed through SQL aggregations and PDF rendering, running the risk of browser timeouts.

**What I Did (And Decided):** 
I moved the heavy lifting out of the request cycle into a custom Node.js in-memory queue. I decided to build the queue from scratch to guarantee idempotency and retries without forcing local Redis dependencies. The API now returns a `202 Accepted` instantly. A background worker queries SQLite, draws the PDF using `pdfkit`, saves it as an artifact, and resolves the job with a download link.

**What Came of It:** 
API latency dropped from 10 seconds to less than 50 milliseconds. The worker safely handles simulated crashes by automatically retrying up to 3 times before triggering an alert, ensuring no report request is ever silently dropped.

---

## 👤 Bio & Contact (CTA Copy)

**The Bio:**
"I'm a backend-focused engineering intern who builds data pipelines that don't break at 3 AM. I write Node.js and Python, and I prefer simple, decoupled architectures over massive frameworks when the job doesn't call for it."

**The CTA:**
"Need pipelines that scale? [Email me to schedule a technical screening]."

---

## ✂️ The Editing Test (Before vs. After)

I prompted AI to write my scraper intro, and it gave me generic garbage. I threw it out and rewrote it to sound like my *Voice Card*.

**❌ Generic AI (Before):** 
> *"I am a results-driven professional leveraging cutting-edge web scraping technologies to synergize big data extraction and empower data-driven paradigms for optimal business workflows."*

**✅ My Edited Version (After):**
> *"I build polite web scrapers that pull clean data without getting blocked by rate limits or crashing the target server."*
