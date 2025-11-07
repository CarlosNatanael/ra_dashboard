DROP TABLE IF EXISTS review_queue;

CREATE TABLE review_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    game_name TEXT NOT NULL,
    developer_username TEXT NOT NULL,
    date_requested TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'Pending',
    reviewer_username TEXT
);