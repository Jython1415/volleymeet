-- Create tables
CREATE TABLE IF NOT EXISTS meetings (
    meeting_id CHAR(36) PRIMARY KEY,
    title VARCHAR(2000) NOT NULL,
    details TEXT,
    location VARCHAR(2000),
    date_time DATETIME NOT NULL
);

-- Add some sample data for testing
INSERT INTO
    meetings (meeting_id, title, details, location, date_time)
VALUES
    (
        '1',
        'Meeting 1',
        'Details for meeting 1',
        'Location 1',
        '2021-01-01 10:00:00'
    ),
    (
        '2',
        'Meeting 2',
        'Details for meeting 2',
        'Location 2',
        '2021-01-02 11:00:00'
    ),
    (
        '3',
        'Meeting 3',
        'Details for meeting 3',
        'Location 3',
        '2021-01-03 12:00:00'
    );