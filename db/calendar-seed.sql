-- Creating Calendars table
CREATE TABLE IF NOT EXISTS calendars (
    calendar_id CHAR(36) PRIMARY KEY,
    title VARCHAR(2000) NOT NULL,
    details TEXT CHECK (LENGTH(details) <= 10000)
);

-- Creating Triggers for Auto-generating UUIDs
-- Trigger for Calendars table
DELIMITER $$
CREATE TRIGGER before_insert_calendar 
BEFORE INSERT ON calendars 
FOR EACH ROW 
BEGIN 
    IF NEW.calendar_id IS NULL THEN
        SET NEW.calendar_id = UUID();
    END IF;
END$$
DELIMITER ;

-- Inserting Seed Data for Testing
-- Insert into Calendars
INSERT INTO
    calendars (calendar_id, title, details)
VALUES
    ('c1', 'Work Calendar', 'All work-related events'),
    ('c2', 'Personal Calendar', 'Personal appointments');
