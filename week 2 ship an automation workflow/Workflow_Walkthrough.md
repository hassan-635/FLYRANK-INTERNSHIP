# Week 2: Ship an Automation Workflow v2

## 🎯 The Target Workflow: "Draft, Critique, Revise" (PR Generation)
**Context from FL-01 Audit:** Writing Pull Request (PR) descriptions is a repetitive task that requires context gathering, drafting, and formatting to meet team standards.

---

## 🗺️ Step Diagram
`[Git Diff]` ➡️ **Step 1: Gather** ➡️ **Step 2: Draft (AI)** ➡️ **Step 3: Critique (AI)** ➡️ **Step 4: Format (AI)** ➡️ `[Final PR Markdown]`

---

## 🛠️ The Build (Claude Project Setup)
I built this using a **Claude Project** equipped with a strict set of custom instructions to act as a chaining system.

### **Prompt Chain Instructions:**
1. **Prompt 1 (Gather & Draft):** *"Here is my git diff. Write a draft PR description explaining the 'why' behind these changes, not just the 'what'. Do not use formatting yet."*
2. **Prompt 2 (Critique):** *"Act as a Senior Engineer reviewing this draft PR description. Does it pass our 3-point checklist? 1. Is the business value clear? 2. Are breaking changes highlighted? 3. Are testing instructions included? Critique the draft."*
3. **Prompt 3 (Revise & Format):** *"Revise the draft based on your critique. Output the final version using standard GitHub markdown with ## Headers and bullet points."*

---

## ⏱️ The 5 Real Runs (Time Accounting)

**Manual Baseline:** It usually takes me **10-12 minutes** to review my own diff, remember what I did 3 days ago, and write a thorough, formatted PR description.

| Run | Input (Git Diff) | Setup/Run Time | Output Quality | Time Saved |
|---|---|---|---|---|
| **Run 1** | Adding caching to Express route | 2 mins | Perfect. Caught that the cache expiration needed explaining in the PR. | 8 mins |
| **Run 2** | Refactoring legacy auth middleware | 3 mins | Critique step noted I didn't include testing instructions. Re-prompted for it. | 9 mins |
| **Run 3** | Updating NPM dependencies | 1 min | Skipped critique step (too simple). Instantly formatted perfectly. | 9 mins |
| **Run 4** | Web Scraper (Task 3) | 2 mins | Excellent summary of the backoff retry logic. | 10 mins |
| **Run 5** | Background Job Queue (Week 6) | 2.5 mins | Perfect. Highlighted the `better-queue` implementation clearly. | 9.5 mins |

**Total Time Saved per week (avg 5 PRs):** ~45 minutes.

---

## ⚠️ Known Failure Points & Human Review Needed

1. **Missing Business Context:** A `git diff` only shows code changes. It does not show *why* the product manager requested the feature. **Human Review Needed:** I must manually inject a one-line business reason before hitting "Draft" (e.g., "Added caching because the marketing page was slow during the campaign").
2. **Testing Instructions hallucination:** If my diff doesn't include new unit tests, the AI will sometimes guess how to test it manually, and the guess is often wrong. **Human Review Needed:** Always manually verify the "How to Test" section before clicking Create PR.
3. **Token Limits on Huge Diffs:** If the PR is a massive 50-file refactor, pasting the raw diff breaks the context window. At that point, the workflow fails and I have to summarize it myself.
