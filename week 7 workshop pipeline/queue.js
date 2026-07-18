const { v4: uuidv4 } = require('uuid');
const EventEmitter = require('events');

class JobQueue extends EventEmitter {
    constructor() {
        super();
        this.jobs = new Map(); 
        this.idempotencyMap = new Map(); 
        this.queue = []; 
        this.isProcessing = false;
        
        // Configuration
        this.MAX_RETRIES = 3;
    }

    /**
     * Add a job to the queue. Handles idempotency.
     */
    addJob(data, idempotencyKey) {
        if (idempotencyKey && this.idempotencyMap.has(idempotencyKey)) {
            const existingJobId = this.idempotencyMap.get(idempotencyKey);
            console.log(`[QUEUE] Idempotency hit for key '${idempotencyKey}'. Returning existing Job ID: ${existingJobId}`);
            return existingJobId;
        }

        const jobId = uuidv4();
        
        this.jobs.set(jobId, {
            id: jobId,
            status: 'pending', 
            data: data,
            result: null, // This will eventually hold the URL to the PDF artifact
            error: null,
            retries: 0,
            createdAt: new Date().toISOString()
        });

        if (idempotencyKey) {
            this.idempotencyMap.set(idempotencyKey, jobId);
        }

        this.queue.push(jobId);
        console.log(`[QUEUE] Added new report generation job: ${jobId}`);

        this.processQueue();

        return jobId;
    }

    getJobStatus(jobId) {
        return this.jobs.get(jobId) || null;
    }

    registerWorker(workerFunction) {
        this.workerFunction = workerFunction;
    }

    async processQueue() {
        if (this.isProcessing || this.queue.length === 0) return;
        
        this.isProcessing = true;

        while (this.queue.length > 0) {
            const jobId = this.queue.shift();
            const job = this.jobs.get(jobId);

            if (!job) continue;

            job.status = 'active';
            console.log(`\n[WORKER] Picked up job ${jobId}. Generating PDF Report...`);

            try {
                // Pass jobId to the worker so it can name the artifact
                const result = await this.workerFunction(job.data, jobId);
                
                job.status = 'completed';
                job.result = result;
                console.log(`[WORKER] ✅ Job ${jobId} completed successfully. Report generated.`);
                
            } catch (error) {
                job.retries += 1;
                console.error(`[WORKER] ⚠️ Job ${jobId} failed. Attempt ${job.retries}/${this.MAX_RETRIES}. Error: ${error.message}`);
                
                if (job.retries < this.MAX_RETRIES) {
                    job.status = 'pending';
                    this.queue.unshift(jobId);
                    console.log(`[QUEUE] Re-queued job ${jobId} for retry.`);
                } else {
                    job.status = 'failed';
                    job.error = error.message;
                    console.error(`[ALERT] 🚨 Job ${jobId} failed permanently! Human intervention needed.`);
                }
            }
        }

        this.isProcessing = false;
    }
}

module.exports = new JobQueue();
