# Week 2: Prompting Fundamentals on Real Tasks

**Target Task (from FL-01):** Writing comprehensive unit tests for backend APIs.

---

## 🪜 The Prompt Iteration Log

### 🔴 0. The Naive Baseline
**Prompt:** *"Write unit tests for this Express route. [Code]"*
**Output Summary:** Generated a generic Jest test suite using `supertest`. It checked if the endpoint returned a `200 OK` status, but it failed to mock the database, resulting in tests that would actually hit the production database if executed.
**Note on Output Difference:** The output was functionally useless for a real codebase because it lacked isolated database mocks and ignored edge cases entirely.

### 🟡 1. Adding Technique: Role Assignment
**Prompt:** *"Act as a Senior Backend QA Automation Engineer. Write unit tests for this Express route. [Code]"*
**Output Summary:** The tone shifted dramatically. The output included tests for a `400 Bad Request` and `500 Server Error`. It added basic `jest.mock()` statements.
**Note on Output Difference:** By assigning a senior QA role, the AI shifted from "write a script that runs" to "write code that verifies stability." The edge cases improved, but the mocks were still hallucinated and didn't match my specific ORM.

### 🟡 2. Adding Technique: Context and Motivation
**Prompt:** *"[Role] The context is that this is a critical payment processing route. A failure here could result in double-charging a user. Write the tests. [Code]"*
**Output Summary:** Added a highly specific test case: `it('should rollback the database transaction if the third-party payment gateway fails')`.
**Note on Output Difference:** Giving the AI the *business stakes* forced it to look for logical flaws (like database transactions) rather than just syntax errors. The output became significantly more rigorous.

### 🟡 3. Adding Technique: Few-Shot Examples
**Prompt:** *"[Role/Context] Here is an example of exactly how we mock our database layer in our codebase: `jest.mock('../db', () => ({ transaction: jest.fn(), ... }))`. Write the tests. [Code]"*
**Output Summary:** The AI adopted the exact mocking syntax provided in the example, dropping its previous generic `jest.mock()` hallucinations.
**Note on Output Difference:** The generated code became immediately copy-pasteable. Instead of spending 10 minutes fixing the AI's generic mocks, the output matched my codebase's exact architectural patterns.

### 🟡 4. Adding Technique: Step Decomposition (Chain of Thought)
**Prompt:** *"[Role/Context/Example] Think step by step. First, list out all the edge cases you plan to test. Second, write the mocks. Third, write the actual test suite."*
**Output Summary:** The AI outputted a bulleted list of 6 edge cases *before* writing any code. By thinking out loud, it realized it needed to test for missing authentication headers—an edge case it completely missed in versions 1 through 3.
**Note on Output Difference:** Forcing the AI to plan before coding improved the actual logic of the tests. The output was much longer but vastly more comprehensive.

### 🟢 5. Adding Technique: Output Structure
**Prompt:** *"[All previous] Output your response using exactly these XML tags: `<edge_cases>`, `<mocks>`, `<test_suite>`."*
**Output Summary:** The response was perfectly clean, wrapped exactly in the requested XML tags with no conversational filler ("Here are your tests!").
**Note on Output Difference:** The output became highly predictable and machine-readable, making it trivial to extract just the code block without scrolling through chatty AI text.

---

## ⚔️ Cross-Model Comparison (Claude vs ChatGPT)

I ran the final Version 5 prompt on both **Claude 3.5 Sonnet** and **ChatGPT (GPT-4o)**.

- **Structure & Formatting:** Claude followed the XML tag output structure flawlessly. ChatGPT ignored the `<test_suite>` XML tag and reverted to its standard markdown ` ```javascript ` code blocks instead.
- **Accuracy (The Mocks):** Both accurately applied the few-shot examples. However, Claude's step decomposition was slightly more analytical—it caught a subtle race-condition edge case that ChatGPT glossed over.
- **Tone:** ChatGPT included conversational filler ("Sure! As a Senior QA Engineer, here is your robust test suite..."). Claude adhered strictly to the XML constraints and provided zero fluff.
- **Conclusion:** For strict formatting and complex logical edge cases, Claude won. ChatGPT was fine for the code itself but failed the structural constraints (XML tags).

---

## 🏆 Final Reusable Prompt Template

```text
Act as a Senior Backend QA Automation Engineer. I need you to write comprehensive unit tests for the provided backend code.

Context: 
[Insert business context here, e.g., This is a critical auth route, failure means data leaks.]

Example of our mocking pattern:
[Insert a small snippet of how you mock your DB or external services here]

Follow these instructions exactly:
1. First, think through all possible edge cases, failure states, and security vulnerabilities.
2. Second, write the necessary mocks based on the provided example.
3. Third, write the complete Jest test suite.

Output your response using ONLY the following XML tags, with no conversational filler outside of them:
<edge_cases>
(your planning goes here)
</edge_cases>

<mocks>
(your mock code goes here)
</mocks>

<test_suite>
(your test suite code goes here)
</test_suite>

Code to test:
[Insert Code Here]
```
