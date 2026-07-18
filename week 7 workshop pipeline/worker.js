const sqlite3 = require('sqlite3').verbose();
const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');
const jobQueue = require('./queue');

const dbPath = path.join(__dirname, 'books.db');
const reportsDir = path.join(__dirname, 'reports');

// Ensure reports directory exists for Artifact Handling
if (!fs.existsSync(reportsDir)) {
    fs.mkdirSync(reportsDir, { recursive: true });
}

/**
 * Executes a SQL query and returns a Promise.
 */
function queryDB(query) {
    return new Promise((resolve, reject) => {
        const db = new sqlite3.Database(dbPath, (err) => {
            if (err) return reject(err);
        });

        db.all(query, [], (err, rows) => {
            db.close();
            if (err) return reject(err);
            resolve(rows);
        });
    });
}

/**
 * The heavy worker task: Queries DB, Aggregates data, Renders PDF.
 */
async function generatePDFReport(data, jobId) {
    // 1. SQL Aggregation (Data Query)
    // We are querying the SQLite DB built from the web scraper task
    const sql = `
        SELECT 
            category, 
            COUNT(id) as book_count, 
            ROUND(AVG(price), 2) as avg_price, 
            SUM(stock_count) as total_stock
        FROM books 
        GROUP BY category 
        ORDER BY book_count DESC
    `;
    
    console.log(`[WORKER] Running SQL Aggregation for job ${jobId}...`);
    const rows = await queryDB(sql);

    // Simulate heavy rendering by adding a deliberate delay (2-4 seconds)
    // and a 20% random failure chance to demonstrate retries
    await new Promise((res, rej) => {
        setTimeout(() => {
            if (Math.random() < 0.20) {
                rej(new Error("Simulated random rendering engine crash (Timeout)"));
            } else {
                res();
            }
        }, Math.floor(Math.random() * 2000) + 2000);
    });

    // 2. Render PDF Report (Artifact Generation)
    return new Promise((resolve, reject) => {
        const doc = new PDFDocument({ margin: 50 });
        const fileName = `report_${jobId}.pdf`;
        const filePath = path.join(reportsDir, fileName);
        
        const stream = fs.createWriteStream(filePath);
        doc.pipe(stream);

        // Header
        doc.fontSize(24).text('FlyRank Inventory Report', { align: 'center' });
        doc.moveDown();
        doc.fontSize(12).fillColor('gray').text(`Generated on: ${new Date().toLocaleString()}`, { align: 'center' });
        doc.text(`Job ID: ${jobId}`, { align: 'center' });
        doc.moveDown(2);

        // Table Header
        doc.fillColor('black').fontSize(14).text('Category Breakdown', { underline: true });
        doc.moveDown();
        
        doc.fontSize(12);
        const startY = doc.y;
        doc.text('Category', 50, startY, { width: 200 });
        doc.text('Books', 250, startY, { width: 100 });
        doc.text('Avg Price', 350, startY, { width: 100 });
        doc.text('Total Stock', 450, startY, { width: 100 });
        doc.moveDown();
        
        doc.moveTo(50, doc.y).lineTo(550, doc.y).stroke();
        doc.moveDown(0.5);

        // Table Rows
        doc.fontSize(10);
        let yPos = doc.y;
        
        rows.forEach((row, index) => {
            // Check page overflow
            if (yPos > 700) {
                doc.addPage();
                yPos = 50;
            }

            doc.text(row.category || 'Unknown', 50, yPos, { width: 200 });
            doc.text(row.book_count.toString(), 250, yPos, { width: 100 });
            doc.text(`£${row.avg_price}`, 350, yPos, { width: 100 });
            doc.text(row.total_stock.toString(), 450, yPos, { width: 100 });
            
            yPos += 20;
        });

        doc.end();

        stream.on('finish', () => {
            // 3. Artifact Handling: Store the file, return the LINK
            const reportUrl = `/reports/${fileName}`;
            resolve({
                message: "PDF Report successfully generated.",
                total_categories: rows.length,
                download_url: reportUrl
            });
        });

        stream.on('error', (err) => {
            reject(err);
        });
    });
}

// Register worker with queue
jobQueue.registerWorker(generatePDFReport);

module.exports = {
    startWorker: () => console.log("🤖 PDF Report Worker registered and listening...")
};
