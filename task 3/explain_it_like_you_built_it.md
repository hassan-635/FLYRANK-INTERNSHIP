# 🧠 Explain It Like You Built It — Web Scraper

## The Piece I'm Explaining: How Star Ratings Are Hidden Inside CSS Class Names (Not Visible Text!)

---

So here's something that genuinely surprised me while building my scraper.

When you go to [books.toscrape.com](https://books.toscrape.com) and look at a book, you see those little stars — like 3 out of 5 stars. You'd think, okay, somewhere in the HTML there's text that says "3" or "Three stars", right? That's what I assumed.

**Nope.**

When I actually looked at the raw HTML (right-click → View Page Source), I found this:

```html
<p class="star-rating Three">
    <i class="icon-star"></i>
    <i class="icon-star"></i>
    <i class="icon-star"></i>
    <i class="icon-star"></i>
    <i class="icon-star"></i>
</p>
```

See what's going on? There are **always 5 star icons** regardless of the rating. The actual rating — the word `Three` — is stuffed inside the **class name** of the `<p>` tag. Not in the text. Not in a data attribute. In the *class*.

The CSS on the website then uses that class name to decide how many stars to color gold vs. gray. So `star-rating Three` means "color 3 stars gold, leave 2 gray." The browser does this styling automatically — but as a scraper, I don't see CSS styling. I only see the raw HTML.

So the question became: **how do I pull the word "Three" out of a class name and turn it into the number 3?**

Here's how I solved it in my `parser.py`:

```python
STAR_RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

star_tag = soup.select_one("p.star-rating")
classes = star_tag.get("class", [])  # Returns: ["star-rating", "Three"]

for cls in classes:
    if cls in STAR_RATING_MAP:
        rating = STAR_RATING_MAP[cls]  # "Three" → 3
```

Let me break that down like I'd explain to a friend:

1. **`soup.select_one("p.star-rating")`** — This tells BeautifulSoup: "go find me the `<p>` tag that has `star-rating` in its class." Think of it like Ctrl+F but smarter — it understands HTML structure.

2. **`.get("class", [])`** — This pulls out ALL the classes on that tag as a list. So `class="star-rating Three"` becomes `["star-rating", "Three"]`.

3. **The loop** — I go through each class name and check: is this word in my dictionary? `"star-rating"` isn't in the dictionary, skip. `"Three"` IS in the dictionary → map it to `3`. Done.

The **dictionary** (`STAR_RATING_MAP`) is basically a translation table — English words to numbers. Simple, but without it, I'd have messy text instead of clean data.

### Why this matters for the bigger picture:

This is a tiny example of what scraping actually is. The data you *want* (a number: 3) is almost never sitting there in a nice format. It's hiding in weird places — class names, URL slugs, nested tags, inconsistent text with random whitespace. The whole job of the parser is to **find where the data is actually hiding and pull it into something clean and structured**.

And this same pattern repeated across every single field I extracted. Prices had `£` signs and sometimes weird `Â` characters that needed stripping. Stock counts were buried in sentences like `"In stock (22 available)"` — I had to use a regex to fish out just the `22`. The book's category wasn't on the product section at all — it was in the breadcrumb navigation at the top of the page.

**Scraping isn't just downloading pages. It's detective work — figuring out where the website hid the data, and writing code smart enough to find it every time.**

---

*Built as part of FlyRank Internship Task 3 — Ethical Web Scraper*
*GitHub: https://github.com/hassan-635/FLYRANK-INTERNSHIP*
