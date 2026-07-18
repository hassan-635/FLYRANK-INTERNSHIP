const { v4: uuidv4 } = require('uuid');
const EventEmitter = require('events');

class JobQueue extends EventEmitter {
    constructor() {
        super();
        this.jobs = new Map(); // Store job details: { id, status, data, result, error, retries }
        this.idempotencyMap = new Map(); // Maps idempotencyKey -> jobId
        this.queue = []; // Array of jobIds waiting to be processed
        this.isProcessing = false;
        
        // Configuration
        this.MAX_RETRIES = 3;
    }

    /**
     * Add a job to the queue. Handles idempotency.
     * @param {Object} data - The payload
     * @param {String} idempotencyKey - Unique key to prevent duplicates
     * @returns {String} jobId
     */
    addJob(data, idempotencyKey) {
        // Idempotency Check: If we already have a job for this key, return the existing jobId
        if (idempotencyKey && this.idempotencyMap.has(idempotencyKey)) {
            const existingJobId = this.idempotencyMap.get(idempotencyKey);
            console.log(`[QUEUE] Idempotency hit for key '${idempotencyKey}'. Returning existing Job ID: ${existingJobId}`);
            return existingJobId;
        }

        const jobId = uuidv4();
        
        this.jobs.set(jobId, {
            id: jobId,
            status: 'pending', // pending, active, completed, failed
            data: data,
            result: null,
            error: null,
            retries: 0,
            createdAt: new Date().toISOString()
        });

        if (idempotencyKey) {
            this.idempotencyMap.set(idempotencyKey, jobId);
        }

        this.queue.push(jobId);
        console.log(`[QUEUE] Added new job: ${jobId}`);

        // Trigger processing loop if not already running
        this.processQueue();

        return jobId;
    }

    /**
     * Get job status
     */
    getJobStatus(jobId) {
        return this.jobs.get(jobId) || null;
    }

    /**
     * Registers the worker function to process jobs
     */
    registerWorker(workerFunction) {
        this.workerFunction = workerFunction;
    }

    /**
     * Internal loop to process the queue
     */
    async processQueue() {
        if (this.isProcessing || this.queue.length === 0) return;
        
        this.isProcessing = true;

        while (this.queue.length > 0) {
            const jobId = this.queue.shift();
            const job = this.jobs.get(jobId);

            if (!job) continue;

            job.status = 'active';
            console.log(`\n[WORKER] Picked up job ${jobId}. Executing...`);

            try {
                // Execute the actual heavy work
                const result = await this.workerFunction(job.data);
                
                job.status = 'completed';
                job.result = result;
                console.log(`[WORKER] ✅ Job ${jobId} completed successfully.`);
                
            } catch (error) {
                job.retries += 1;
                console.error(`[WORKER] ⚠️ Job ${jobId} failed. Attempt ${job.retries}/${this.MAX_RETRIES}. Error: ${error.message}`);
                
                if (job.retries < this.MAX_RETRIES) {
                    // Retry: Push back to the front of the queue
                    job.status = 'pending';
                    this.queue.unshift(jobId);
                    console.log(`[QUEUE] Re-queued job ${jobId} for retry.`);
                } else {
                    // Permanent failure (Alert required)
                    job.status = 'failed';
                    job.error = error.message;
                    console.error(`[ALERT] 🚨 Job ${jobId} failed permanently after ${this.MAX_RETRIES} retries! Human intervention needed.`);
                }
            }
        }

        this.isProcessing = false;
    }
}

module.exports = new JobQueue();
