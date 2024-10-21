-- Creating Meetings table
CREATE TABLE IF NOT EXISTS meetings (
    meeting_id CHAR(36) PRIMARY KEY,
    title VARCHAR(2000) NOT NULL,
    details TEXT CHECK (LENGTH(details) <= 10000),
    location VARCHAR(2000),
    date_time CHAR(20) NOT NULL
);

-- Creating Triggers for Auto-generating UUIDs
-- Trigger for Meetings table
DELIMITER $$
CREATE TRIGGER before_insert_meeting 
BEFORE INSERT ON meetings 
FOR EACH ROW 
BEGIN 
    IF NEW.meeting_id IS NULL THEN
        SET NEW.meeting_id = UUID();
    END IF;
END$$
DELIMITER ;

-- Inserting Seed Data for Testing
-- Insert into Meetings
INSERT INTO
    meetings (meeting_id, title, details, location, date_time)
VALUES
    (
        'm1',
        'Team Meeting',
        'Discuss roadmap',
        'Conf Room 1',
        '2024-10-01 09:00'
    ),
    (
        'm2',
        'Client Meeting',
        'Review requirements',
        'Online',
        '2024-10-02 14:00'
    );