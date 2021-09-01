DROP TABLE IF EXISTS url;

CREATE TABLE url (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    shortened_url TEXT UNIQUE NOT NULL,
    full_url TEXT NOT NULL
);