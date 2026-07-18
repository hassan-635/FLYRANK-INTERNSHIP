const express = require('express');
const cors = require('cors');
const path = require('path');
const jobQueue = require('./queue');
const { startWorker } = require('./worker'); 

const app = express();
app.use(express.json());
app.use(cors());

// Serve the generated PDF reports statically
app.use('/reports', express.static(path.join(__dirname, 'reports')));

startWorker();

/**
 * 1. The Accept Endpoint
 * Initiates the Background Job for generating the PDF report
 */
app.post('/api/reports/generate', (req, res) => {
    const data = req.body || {};
    
    // Idempotency: Use client provided key or default to a generic "daily-report" key
    // In a real app, this might be "report-2023-10-01" to prevent double generating today's report
    const idempotencyKey = req.headers['idempotency-key'] || `report-${new Date().toISOString().split('T')[0]}`;

    // Add to queue
    const jobId = jobQueue.addJob(data, idempotencyKey);

    return res.status(202).json({
        message: "Report generation accepted. Processing in background.",
        jobId: jobId,
        statusUrl: `/api/reports/status/${jobId}`
    });
});

/**
 * 2. The Status Endpoint
 * Polling endpoint to check report generation status and get the download link.
 */
app.get('/api/reports/status/:id', (req, res) => {
    const jobId = req.params.id;
    const job = jobQueue.getJobStatus(jobId);

    if (!job) {
        return res.status(404).json({ error: "Job not found." });
    }

    return res.status(200).json({
        jobId: job.id,
        status: job.status,      
        retries: job.retries,
        createdAt: job.createdAt,
        result: job.result,      // This contains the `download_url` if completed
        error: job.error         
    });
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
    console.log(`\n===========================================`);
    console.log(`🚀 Week 7 Workshop Pipeline API on port ${PORT}`);
    console.log(`===========================================\n`);
});
