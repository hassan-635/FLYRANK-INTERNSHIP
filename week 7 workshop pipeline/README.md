# Week 7: Workshop Pipeline — Background Report Generation

This project brings together everything from the last month into a single professional pipeline. It queries an SQLite database, aggregates the data via SQL, dynamically generates a PDF report, handles the PDF as a stored artifact, and processes the whole thing inside a background job queue to ensure the API stays lightning fast.

## 🎯 What it does

1. **SQL Aggregation:** Queries the `books` database (populated from the Week 3 scraper data) to calculate the total book count, average price, and total stock grouped by category.
2. **Artifact Handling:** Instead of trying to send a massive PDF binary back in a JSON response, the worker generates the PDF, saves it to the `reports/` folder, and returns a clean URL link to download it.
3. **Background Job Pattern:** 
   - `POST /api/reports/generate` returns `202 Accepted` instantly.
   - The worker picks up the job, simulates a heavy PDF render, handles random failures (with 3 automatic retries), and creates the report.
   - `GET /api/reports/status/:id` allows the client to poll until the `download_url` is ready.

## 🚀 How to Run

1. **Install Dependencies:**
   ```bash
   npm install
   ```

2. **Initialize the Database:**
   *(This reads the scraped `books.json` from the Task 3 folder and populates a local SQLite database)*
   ```bash
   node init_db.js
   ```

3. **Start the Server & Worker:**
   ```bash
   node server.js
   ```

4. **Generate a Report:**
   ```bash
   curl -X POST http://localhost:4000/api/reports/generate \
     -H "Content-Type: application/json" \
     -d "{}"
   ```

5. **Check the Status:**
   Grab the `jobId` from the previous response and hit the status endpoint:
   ```bash
   curl http://localhost:4000/api/reports/status/YOUR_JOB_ID
   ```

6. **Download the PDF:**
   Once the status is `completed`, grab the `download_url` from the `result` object and open it in your browser:
   `http://localhost:4000/reports/report_YOUR_JOB_ID.pdf`
