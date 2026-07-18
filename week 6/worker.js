const jobQueue = require('./queue');

/**
 * Simulates a slow, unpredictable "A6 AI call".
 * Takes 5-10 seconds to run.
 * Randomly fails 30% of the time to demonstrate retries and alerts.
 */
async function slowAICall(data) {
    return new Promise((resolve, reject) => {
        // Random execution time between 5s and 10s
        const executionTime = Math.floor(Math.random() * 5000) + 5000;
        
        setTimeout(() => {
            // Simulate a random failure (30% chance)
            if (Math.random() < 0.30) {
                return reject(new Error("External AI API Rate Limit Exceeded or Timeout (Simulated)"));
            }

            // Success case
            resolve({
                generated_text: `AI analyzed your prompt: "${data.prompt}". Output generated in ${executionTime/1000} seconds.`,
                confidence: 0.98
            });
        }, executionTime);
    });
}

// Register this worker function with the queue
jobQueue.registerWorker(slowAICall);

module.exports = {
    startWorker: () => console.log("🤖 Worker registered and listening for jobs...")
};
