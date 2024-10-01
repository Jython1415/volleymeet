-- Create tables
CREATE TABLE IF NOT EXISTS meetings (
    meeting_id CHAR(36) PRIMARY KEY,
    title VARCHAR(2000) NOT NULL,
    details TEXT,
    location VARCHAR(2000),
    date_time DATETIME NOT NULL
);
