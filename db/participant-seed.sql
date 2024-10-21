-- Creating Participants table
CREATE TABLE IF NOT EXISTS participants (
    participant_id CHAR(36) PRIMARY KEY,
    name VARCHAR(600) NOT NULL,
    email VARCHAR(255) NOT NULL CHECK (email LIKE '%_@__%.__%')
);

-- Creating Triggers for Auto-generating UUIDs
-- Trigger for Participants table
DELIMITER $$
CREATE TRIGGER before_insert_participant 
BEFORE INSERT ON participants 
FOR EACH ROW 
BEGIN 
    IF NEW.participant_id IS NULL THEN
        SET NEW.participant_id = UUID();
    END IF;
END$$
DELIMITER ;

-- Inserting Seed Data for Testing
-- Insert into Participants
INSERT INTO
    participants (participant_id, name, email)
VALUES
    ('p1', 'Alice Johnson', 'alice.j@example.com'),
    ('p2', 'Bob Smith', 'bob.smith@example.com');