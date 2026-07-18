# Week 2: The Prompt Ladder

## 🔴 The Baseline (Embarrassing, Lazy Prompt)
**Prompt:** *"Write a backend API to upload a file."*
**Output Excerpt:** Provided a generic Python/Flask script using `request.files` and saving to a local `uploads/` directory on the server.

---

## 🪜 Version 1: Adding Context (Tech Stack & Details)
**Prompt:** *"Write a backend API to upload a file. The file is a 50MB PDF report and we are using Node.js with Express."*
**Output Excerpt:** Provided an Express boilerplate using the `multer` middleware, specifically configuring the `limits: { fileSize: 50 * 1024 * 1024 }` setting, saving to a local `uploads/` folder.

- **What changed in the prompt:** I added context about the tech stack (Node/Express) and the specific file size (50MB).
- **What improved in the output:** It stopped guessing the language (giving me Python) and automatically configured the `multer` size limits so a 50MB file wouldn't throw a default size error.
- **What still failed:** It's still writing the file to the local disk of the server, which is an anti-pattern for modern cloud deployments.
- **What I'd try next:** Add a constraint to prevent local disk storage.

---

## 🪜 Version 2: Adding Constraints
**Prompt:** *"Write a backend API to upload a 50MB PDF report in Node.js/Express. Constraint: Do not save the file to local disk, use memory storage before processing."*
**Output Excerpt:** Switched the multer configuration to `multer.memoryStorage()`. The route handler accessed the file via `req.file.buffer`.

- **What changed in the prompt:** I added a negative constraint ("do not save to local disk").
- **What improved in the output:** The code successfully avoided writing to the filesystem.
- **What still failed (The "Made it Worse" moment):** This actually made the architecture *worse*. Holding a 50MB PDF in a Node.js Buffer blocks the event loop and eats up RAM. If 10 users upload at once, the server crashes. 
- **What I'd try next:** Clarify the actual architectural goal: streaming it directly to a cloud bucket.

---

## 🪜 Version 3: Adding a Clear Goal / Architecture
**Prompt:** *"Write a Node.js/Express API to upload a 50MB PDF. Goal: Stream the upload directly to an AWS S3 bucket without holding the entire file in memory or saving it to disk."*
**Output Excerpt:** Used the `multer-s3` package along with `@aws-sdk/client-s3`. Provided code that pipes the incoming multipart stream directly up to S3 chunk-by-chunk.

- **What changed in the prompt:** I explicitly stated the architectural goal (streaming directly to S3).
- **What improved in the output:** It finally generated production-ready, scalable code that doesn't crash the server or bloat the local disk!
- **What still failed:** The error handling was sloppy. If S3 timed out, it threw an unhandled promise rejection or returned a raw HTML stack trace to the client.
- **What I'd try next:** Specify a strict output format for the API responses so the frontend can read the errors.

---

## 🪜 Version 4: Adding a Specified Output Format
**Prompt:** *"Write a Node.js/Express API to stream a 50MB PDF upload directly to AWS S3. Format all API responses as standard JSON with 'success', 'message', and 'data' or 'error' fields."*
**Output Excerpt:** Wrapped the upload logic in a `try/catch` block. Sent `res.status(500).json({ success: false, error: err.message })` on failure, and `{ success: true, data: { fileUrl: ... } }` on success.

- **What changed in the prompt:** I demanded a specific JSON structure for all API returns.
- **What improved in the output:** The API now returns predictable, frontend-friendly JSON instead of raw stack traces, making it actually usable by a frontend developer.
- **What still failed:** The code is great, but running it is impossible without knowing exactly what AWS environment variables and IAM permissions to set up.
- **What I'd try next:** Add a requirement for external setup instructions.

---

## 🪜 Version 5: Adding Verification/Setup Requirements
**Prompt:** *"Write a Node.js/Express API to stream a 50MB PDF upload directly to AWS S3. Format API responses as standard JSON. Include a checklist of exactly what AWS IAM permissions and environment variables are required to make this code run."*
**Output Excerpt:** Provided the flawless streaming code, PLUS a markdown checklist stating I need `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, and specifically the `s3:PutObject` IAM permission on the target bucket.

- **What changed in the prompt:** I added a verification/setup requirement (a checklist of external dependencies).
- **What improved in the output:** It stopped assuming I had perfectly configured AWS infrastructure and gave me the exact IAM policy JSON and ENV keys I needed to prevent an "Access Denied" error on my first run.
- **What still failed:** Nothing major! This is a highly robust, production-ready response.
- **What I'd try next:** Clean it up into a reusable template for my peers.

---

## 🏆 Final Reusable Prompt

*"Act as a Senior Backend Engineer. Write a Node.js/Express API endpoint to stream a large file upload (e.g. 50MB PDF) directly to [Cloud Provider, e.g. AWS S3] without saving it to local disk or holding it fully in memory. Ensure the following:*
*- **Format:** All HTTP responses must be standard JSON containing `success` (boolean), `message`, and `data` or `error` fields.*
*- **Setup:** Provide a checklist of the specific IAM permissions, bucket policies, and Environment Variables required to successfully execute this code in production."*
