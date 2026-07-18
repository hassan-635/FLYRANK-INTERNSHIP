# Week 3: The Through-Line (Map Content & CTAs)

## ⚡ 1. The One-Line Claim
*(I had AI generate 10 variations based on my Week 1 proof statement, and I chose and sharpened this one because it speaks directly to the pain point of my target audience: broken systems).*

> **"I engineer fault-tolerant backend pipelines that scale quietly, so your team doesn't get woken up by server crashes at 3 AM."**

---

## 🗺️ 2. The Content Map (Single Page Architecture)

*Note: In Week 1, we decided on a Single Page Application (SPA) to remove friction. All sections flow vertically down one page.*

### **Section 1: The Hero (Landing)**
- **Content:** The One-Line Claim (above) + A brief sub-headline stating my stack (Node.js, Python, Data Engineering).
- **Call to Action (CTA):** Primary Button: **"Email Me"** *(Ladders up to the One Action).*
- **Secondary CTA:** Text link: "Or scroll to see the proof."

### **Section 2: The Strongest Work (Background Job Pipeline)**
- **Content:** The Week 6/7 Background Report Pipeline Case Study (Problem, Decision, Outcome). Includes the raw terminal screenshot showing retries and idempotency hits.
- **Why it's first:** This proves complex architectural thinking (queues, retries, artifact handling), which is the hardest skill to demonstrate.
- **Call to Action (CTA):** **"Email me to build your next queue"** *(Ladders up to the One Action).*

### **Section 3: The Next Work (The Polite Web Scraper)**
- **Content:** The Week 3 Web Scraper Case Study (Problem, Decision, Outcome). Includes the screenshot of the deployed Vercel dashboard.
- **Why it's second:** Shows data gathering, API interaction, and basic frontend visualization.
- **Call to Action (CTA):** **"View the full code on GitHub"** *(A secondary trust-building action for technical managers).*

### **Section 4: The Trust Layer (About & Contact)**
- **Content:** The real headshot photo + the tight Bio written in Week 2.
- **Call to Action (CTA):** The Final, unavoidable Primary Button: **"Email Me"** *(The ultimate One Action).*

---

## 🧺 3. The "Still Need to Gather" List
To actually build this, I am blocked until I gather the following:

1. **Before/After Timing Metrics:** For the Background Job case study, I need the exact millisecond response time drop when moving the PDF generation to the queue.
2. **Terminal Screenshot:** Need to trigger a failure in the local worker queue and take the raw screenshot of the `[ALERT]` console log.
3. **Headshot:** Need to take a clean, well-lit photo against a blank wall for the Bio section.
