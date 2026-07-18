# Week 6: Background Job Architecture (Queue & Worker Model)

This project demonstrates the "professional pattern for everything slow". Instead of blocking the HTTP request while a heavy AI call runs, this API accepts the request, drops it into a queue, and returns instantly. A background worker picks it up and processes it, and the client can check the status via a separate endpoint.

## 🚀 The Three Non-Negotiables Built-In

1. **Idempotency (No double processing):**
   If you send the exact same prompt twice, or use the same `Idempotency-Key` header, the queue recognizes the duplicate and simply returns the *existing* Job ID. It will not process the same job twice.

2. **Retries (Handling inevitable failures):**
   The mock "A6 AI call" in `worker.js` is programmed to intentionally fail 30% of the time. The queue catches these failures and automatically requeues the job (up to 3 times) before giving up. 

3. **Alerts (Someone must find out):**
   If a job exhausts all 3 retries, it is marked as `failed`, and a high-priority `[ALERT]` is logged to the console simulating a pager/Slack notification.

## 🛠️ Endpoints

### 1. `POST /api/generate` (The 202 Endpoint)
**Body:**
```json
{
  "prompt": "Analyze this data..."
}
```
**Response (Instantly):**
```json
{
  "message": "Request accepted. Processing in background.",
  "jobId": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "statusUrl": "/api/status/f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

### 2. `GET /api/status/:id` (The Polling Endpoint)
**Response (While working or retrying):**
```json
{
  "jobId": "f47ac10b-...",
  "status": "active", // or 'pending'
  "retries": 1,
  "result": null
}
```
**Response (When finished):**
```json
{
  "jobId": "f47ac10b-...",
  "status": "completed",
  "result": {
    "generated_text": "AI analyzed your prompt...",
    "confidence": 0.98
  }
}
```

## 💻 How to Run This

Since professional queues like BullMQ require Redis (which is hard to set up on Windows), this project uses a custom-built, robust in-memory queue manager (`queue.js`) that mimics enterprise queue features exactly without needing you to install Docker or WSL.

1. **Install Dependencies:**
   ```bash
   npm install
   ```

2. **Start the Server & Worker:**
   ```bash
   node server.js
   ```

3. **Test It (in another terminal or Postman):**
   ```bash
   curl -X POST http://localhost:3000/api/generate \
     -H "Content-Type: application/json" \
     -d "{\"prompt\": \"Test my heavy AI worker\"}"
   ```
   *Notice how it returns instantly. Look at your server console to watch the worker pick it up, potentially retry if it hits the 30% failure chance, and complete!*
