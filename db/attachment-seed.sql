-- Creating Attachments table
CREATE TABLE IF NOT EXISTS attachments (
    attachment_id CHAR(36) PRIMARY KEY,
    meeting_id CHAR(36) NOT NULL,
    url TEXT NOT NULL CHECK (url LIKE 'http%://%')
);

-- Creating Triggers for Auto-generating UUIDs
-- Trigger for Attachments table
DELIMITER $$
CREATE TRIGGER before_insert_attachment 
BEFORE INSERT ON attachments 
FOR EACH ROW 
BEGIN 
    IF NEW.attachment_id IS NULL THEN
        SET NEW.attachment_id = UUID();
    END IF;
END$$
DELIMITER ;

-- Inserting Seed Data for Testing
-- Insert into Attachments
INSERT INTO
    attachments (meeting_id, url)
VALUES
    (
        'm1',
        'http://example.com/doc1.pdf'
    ),
    (
        'm2',
        'http://example.com/doc2.pdf'
    );