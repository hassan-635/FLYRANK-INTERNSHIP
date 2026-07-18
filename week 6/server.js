const express = require('express');
const cors = require('cors');
const jobQueue = require('./queue');
const { startWorker } = require('./worker'); // Initializes the worker

const app = express();
app.use(express.json());
app.use(cors());

// Start the worker process (in a real app, this might be a separate Node process)
startWorker();

/**
 * 1. The Accept Endpoint
 * Accepts the job quickly, drops it in the queue, and returns 202 instantly.
 */
app.post('/api/generate', (req, res) => {
    const data = req.body;
    
    if (!data.prompt) {
        return res.status(400).json({ error: "Missing 'prompt' in request body." });
    }

    // Idempotency Key: The client can provide this (e.g., in a header), 
    // but for demonstration, we will use the prompt itself as the idempotency key.
    // If the exact same prompt is sent, it won't queue twice!
    const idempotencyKey = req.headers['idempotency-key'] || Buffer.from(data.prompt).toString('base64');

    // Add to queue
    const jobId = jobQueue.addJob(data, idempotencyKey);

    // 202 Accepted means: "I got it, but I'm not done yet."
    return res.status(202).json({
        message: "Request accepted. Processing in background.",
        jobId: jobId,
        statusUrl: `/api/status/${jobId}`
    });
});

/**
 * 2. The Status Endpoint
 * Allows the client to poll for the result.
 */
app.get('/api/status/:id', (req, res) => {
    const jobId = req.params.id;
    const job = jobQueue.getJobStatus(jobId);

    if (!job) {
        return res.status(404).json({ error: "Job not found." });
    }

    // Return the current state of the job
    return res.status(200).json({
        jobId: job.id,
        status: job.status,      // 'pending', 'active', 'completed', or 'failed'
        retries: job.retries,
        createdAt: job.createdAt,
        result: job.result,      // Populated only if completed
        error: job.error         // Populated only if permanently failed
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`\n===========================================`);
    console.log(`🚀 Week 6 Server running on port ${PORT}`);
    console.log(`===========================================\n`);
});
