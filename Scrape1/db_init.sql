CREATE TABLE IF NOT EXISTS book (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT,
    price NUMERIC(10, 2),
    genre TEXT
);