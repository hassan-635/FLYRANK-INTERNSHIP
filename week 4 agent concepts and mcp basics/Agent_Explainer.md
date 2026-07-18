# Week 4: Agent Concepts and MCP Basics

## 1. The Distinction: Workflows vs. Agents
The word "agent" is heavily abused in tech marketing, often applied to simple automated scripts. According to Anthropic's *Building Effective Agents*, the distinction comes down to **agency and routing**.

**A Workflow** is a deterministic system. The LLM operates within pre-defined guardrails set by a developer. The path is hardcoded: Step A triggers Step B, which triggers Step C. The LLM performs the cognitive work within those steps (like summarizing or drafting), but it does not get to decide *what step to take next*. 

**An Agent**, on the other hand, is given a goal and a set of tools, and it autonomously decides the path. It uses an LLM to dynamically route tasks, run loops, handle unpredictable errors, and call external APIs until the goal is met. An agent decides its own "Step B."

### Classifying my FL-04 Pipeline
My Week 2 pipeline ("Draft, Critique, Revise" for PR generation) is definitively a **Workflow**, specifically a **Prompt Chain**. The AI does not decide to critique the code; it critiques the code because I manually passed the output of Prompt 1 into Prompt 2. The routing is entirely human-controlled.

---

## 2. What is MCP? (Model Context Protocol)
MCP is the "USB-C port for AI applications." Historically, if you wanted ChatGPT to talk to your local database, and Claude to talk to that same database, you had to write custom, fragile API integrations for each platform. 

MCP solves this by creating an open standard. An MCP Server exposes data, and any MCP-compliant Client (like Claude Desktop) can plug into it instantly. It exposes three core primitives:
1. **Resources:** Static or dynamic data the AI can read, like a local file, a Notion page, or a Slack thread. It gives the AI "context."
2. **Tools:** Executable actions the AI can take. Instead of just reading data, the AI can call a tool to execute a SQL query, fetch a live web page, or push code to GitHub.
3. **Prompts:** Reusable templates exposed by the server that users can invoke to kick off standard tasks.

---

## 3. Upgrading my Workflow into an Agent
To turn my FL-04 Prompt Chain into a true Agent, I would need to give it autonomy via MCP tools. 

**The Concrete Agent Upgrade:** 
Instead of a human manually copying a `git diff` and running three prompts, I would give Claude Desktop an MCP Server connected to Jira and GitHub. 
I would simply say: *"Write and submit a PR for Jira ticket DEV-404."*
The Agent would:
1. Use a Jira MCP Tool to fetch the ticket details (understanding the business context).
2. Use a GitHub MCP Tool to find the associated branch and fetch the diff.
3. If the diff is too large, the Agent would dynamically decide to fetch it file-by-file (Agency).
4. It would draft the PR, review itself, and finally use a GitHub tool to open the PR via the API.
This moves the system from a human-driven pipeline to an autonomous goal-seeker.

---

## 4. MCP Setup & Evidence

I configured the official `mcp-server-sqlite` and `mcp-server-filesystem` using Claude Desktop to allow the AI to interact with my local machine—things a standard web chat cannot do.

*(Note for reviewers: The screenshots below demonstrate the AI utilizing the tool primitives to read and manipulate data outside its training window.)*

### Task 1: Reading Local Filesystem Data
I asked Claude to analyze a local JSON configuration file on my hard drive. Standard chat cannot see my local `C:\` drive. Claude used the MCP filesystem tool to read the contents and summarize it.
> 🖼️ `[ INSERT SCREENSHOT OF CLAUDE USING FILESYSTEM READ TOOL HERE ]`

### Task 2: Querying a Live Local Database
I connected the SQLite MCP server to a local `books.db` file (from Week 3). I asked Claude, *"What is the average price of books in our database?"* Claude autonomously wrote a SQL query, executed it via the MCP tool, and returned the real-time answer.
> 🖼️ `[ INSERT SCREENSHOT OF CLAUDE EXECUTING SQL TOOL HERE ]`

### Task 3: Writing Data Back to Disk
After summarizing the database, I asked Claude to save a markdown report directly to my desktop. Using the filesystem write tool, it created a new `.md` file on my machine without me having to copy-paste anything.
> 🖼️ `[ INSERT SCREENSHOT OF CLAUDE USING FILESYSTEM WRITE TOOL HERE ]`
