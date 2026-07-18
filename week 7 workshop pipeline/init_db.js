const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, 'books.db');
const jsonPath = path.join(__dirname, '../task 3/output/books.json');

// Check if we have the source data
if (!fs.existsSync(jsonPath)) {
    console.error(`[ERROR] Could not find source data at: ${jsonPath}`);
    console.error("Please ensure Task 3 has been run and books.json exists.");
    process.exit(1);
}

// Read the JSON data
console.log(`[INFO] Reading data from ${jsonPath}...`);
const booksData = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
console.log(`[INFO] Found ${booksData.length} books.`);

// Connect to SQLite (creates the file if it doesn't exist)
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('[ERROR] Failed to connect to SQLite:', err.message);
        process.exit(1);
    }
    console.log('[INFO] Connected to SQLite database.');
});

db.serialize(() => {
    // 1. Create Table
    db.run(`DROP TABLE IF EXISTS books`);
    db.run(`
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            price REAL,
            rating INTEGER,
            stock_count INTEGER,
            upc TEXT UNIQUE
        )
    `);
    console.log('[INFO] Created "books" table.');

    // 2. Insert Data
    const stmt = db.prepare(`
        INSERT INTO books (title, category, price, rating, stock_count, upc) 
        VALUES (?, ?, ?, ?, ?, ?)
    `);

    let inserted = 0;
    booksData.forEach((book) => {
        // Fallback for missing fields just in case
        stmt.run(
            book.title || 'Unknown Title',
            book.category || 'Uncategorized',
            book.price_gbp || 0.0,
            book.rating || 0,
            book.stock_count || 0,
            book.upc || `UNKNOWN-${Math.random()}`
        );
        inserted++;
    });

    stmt.finalize();
    console.log(`[INFO] Successfully inserted ${inserted} records into SQLite.`);
});

db.close(() => {
    console.log('[INFO] Database initialization complete! You can now run the worker.');
});
