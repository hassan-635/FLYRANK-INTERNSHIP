# Week 1: Draw the Path (Portfolio Sitemap & Toolkit)

---

## 🧭 1. The Core Strategy
- **My Proof Statement (The Claim):** "I build fast, data-driven backend pipelines and interactive dashboards that turn raw web data into actionable insights."
- **The One Action:** "Email me to build your next data pipeline." (mailto link)

---

## 🗺️ 2. Portfolio Sitemap Sketch
*The absolute minimum pages needed to walk a visitor from landing to the 'One Action'.*

### Page 1: Home (`/`)
- **Hero Section:** States the claim instantly. Large "Email Me" CTA.
- **Why It's Here:** Hook the reader immediately and offer the One Action before they even scroll.

### Page 2: The Work (`/projects`)
- **Content:** Deep dives into the Web Scraper (Task 3) and Background Job Pipeline (Week 6/7).
- **Why It's Here:** This is the *proof* that backs up the claim. Engineering managers need to see the code and architecture. Includes a sticky "Email Me" button at the bottom.

### Page 3: About & Contact (`/about`)
- **Content:** A 3-sentence bio focusing on my tech stack (Node, Python, Data Pipelines) and the final, unmissable contact form/email link.
- **Why It's Here:** Establishes human trust right before they take the One Action.

*(Resisted adding a "Blog" or "Services" page because it distracts from the core claim and action!)*

---

## 🛠️ 3. Free Toolkit Setup
- [x] **Claude:** Account active.
- [x] **ChatGPT:** Account active.
- [x] **Gemini:** Account active.
- [x] **Perplexity:** Account active.

---

## 🧠 4. Claude Project Configuration
- **Project Name:** `Portfolio Build Tutor`
- **Custom Instructions:**
  > "Act as a ruthless, expert technical portfolio tutor. My proof statement is: 'I build fast, data-driven backend pipelines and interactive dashboards that turn raw web data into actionable insights.' My ONE desired action is for an engineering manager to click 'Email Me'. Do not let me add fluff. Pressure test every idea I have against this claim and this one action."

*(Placeholder for Deliverable Submission — Insert Claude Project Screenshot Here)*
> 🖼️ `[ INSERT SCREENSHOT OF CLAUDE PROJECT HERE ]`

---

## 🔥 5. The Pressure Test

### **My Prompt to Claude:**
> "Here is my 3-page sitemap: 1. Home (Hero + CTA), 2. Projects (Proof + CTA), 3. About & Contact (Bio + CTA). Pressure test this against my proof statement and my one action. Is there any friction?"

### **Claude's Output:**
> "It's a good start, but there is still friction. If your goal is to get an engineering manager to email you, why are you making them click to a separate `/projects` page to see your proof? 
> 
> Engineering managers are busy. They won't click through your site.
> 
> **Recommendation:** Kill the 3-page structure. Make it a **Single Page Application (SPA)**. 
> Landing Hero → Scroll down to The Work (Proof) → Scroll down to About/Contact. One continuous flow. Force them to scroll past your proof to get to your bio. It removes navigation friction and keeps them on the path to your 'One Action'."

### **What I Am Changing (The Fix):**
Claude was absolutely right. The 3-page structure adds unnecessary clicks. **I am changing my sitemap to a single, continuous scrolling landing page.** The new path is simply:
`Hero Claim -> Proof (Projects) -> Trust (Bio) -> Action (Email)`
