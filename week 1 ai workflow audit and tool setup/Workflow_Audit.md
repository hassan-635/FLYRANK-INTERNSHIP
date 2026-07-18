# Week 1: AI Workflow Audit and Tool Setup

**Role:** Software Engineering Intern

---

## 📋 1. Workflow Audit (Recurring Tasks)

| # | Recurring Task | Classification | Rationale |
|---|---|---|---|
| 1 | **Deep focused coding on complex business logic** | Just Me | Context is too nuanced and deeply tied to unwritten domain knowledge; explaining it to AI takes longer than writing it. |
| 2 | **Reviewing a peer's Pull Request (PR)** | Just Me | Requires team context, understanding the human intent behind the code, and empathy for constructive feedback. |
| 3 | **Replying to team emails/Slack messages** | Just Me | Tone and personal context are critical; AI often sounds too robotic or misses subtle team cues. |
| 4 | **Generating initial project boilerplate/setup** | Fully Automate | AI is perfect for scaffolding Express servers, React components, or boilerplate configs instantly. |
| 5 | **Writing commit messages** | Fully Automate | AI can read the `git diff` and summarize the changes perfectly without me typing it out. |
| 6 | **Generating mock data for testing** | Fully Automate | Perfect use case for AI to spit out 50 rows of realistic JSON/SQL data instantly. |
| 7 | **Debugging cryptic error messages** | Delegate with review | I paste the stack trace, AI suggests the fix, and I review to ensure it makes sense before applying. |
| 8 | **Writing unit tests for existing functions** | Delegate with review | AI generates excellent edge cases, but I must review to ensure it's testing what actually matters. |
| 9 | **Creating README documentation** | Delegate with review | AI drafts it based on the code, but I tweak it for human readability and structure. |
| 10 | **Brainstorming system architecture** | Collaborate with AI | AI offers different design patterns, but I bounce ideas off it and make the final call based on constraints. |
| 11 | **Refactoring messy code for readability** | Collaborate with AI | I ask AI for suggestions on cleaner patterns, then manually integrate the parts I agree with. |
| 12 | **Learning a new framework/library** | Collaborate with AI | I use AI as an interactive tutor to ask specific "how do I do X in Y" questions rather than reading generic docs. |

---

## 🛠️ 2. Tool Setup & Claude Project

- [x] **ChatGPT Account:** Created & Active
- [x] **Claude Account:** Created & Active
- [x] **Anthropic Academy:** Enrolled in *AI Fluency: Framework & Foundations* (Module 1 completed)

### Claude Project Configuration
**Project Name:** Software Engineering Assistant (Internship)
**Custom Instructions:**
> "You are an expert senior software engineer mentoring a junior intern. I prefer concise, direct answers without fluff. When providing code, always explain the *why* behind your design choices. Focus on best practices for Node.js, Python, and modern web development."

*(Please insert your Claude Project screenshot here before final submission)*
> 🖼️ `[ INSERT SCREENSHOT OF CLAUDE PROJECT HERE ]`

---

## 🎯 3. Target Tasks for FL-02 through FL-04

These are the three specific tasks I will focus on optimizing with AI throughout the internship, along with their success criteria:

### Target Task 1: Generating Initial Project Boilerplates
- **What it is:** Using AI to generate the foundational files, folder structures, and basic configurations (like Express servers or React apps) when starting a new project.
- **"Done Well" Definition:** The generated code runs out-of-the-box without syntax errors, uses the specifically requested tech stack and versions, and saves me at least 15-20 minutes of manual setup time.

### Target Task 2: Writing Comprehensive Unit Tests
- **What it is:** Delegating the creation of Jest/PyTest test suites for specific functions I have written.
- **"Done Well" Definition:** The AI achieves >80% code coverage on the target function, accurately mocks external dependencies, includes at least two non-obvious edge cases, and the tests pass immediately upon execution.

### Target Task 3: Debugging Runtime Errors
- **What it is:** Collaborating with AI by feeding it stack traces and problematic code snippets to find the root cause of an error.
- **"Done Well" Definition:** The AI correctly identifies the root cause on the first or second prompt, and provides a working patch explaining the exact mechanism of the failure, rather than offering generic debugging advice.
