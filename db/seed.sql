-- Creating Meetings table
CREATE TABLE IF NOT EXISTS meetings (
    meeting_id CHAR(36) PRIMARY KEY,
    title VARCHAR(2000) NOT NULL,
    details TEXT CHECK (LENGTH(details) <= 10000),
    location VARCHAR(2000),
    date_time DATETIME NOT NULL
);

-- Creating Participants table
CREATE TABLE IF NOT EXISTS participants (
    participant_id CHAR(36) PRIMARY KEY,
    name VARCHAR(600) NOT NULL,
    email VARCHAR(255) NOT NULL CHECK (email LIKE '%_@__%.__%')
);

-- Creating Calendars table
CREATE TABLE IF NOT EXISTS calendars (
    calendar_id CHAR(36) PRIMARY KEY,
    title VARCHAR(2000) NOT NULL,
    details TEXT CHECK (LENGTH(details) <= 10000)
);

-- Creating Attachments table
CREATE TABLE IF NOT EXISTS attachments (
    attachment_id CHAR(36) PRIMARY KEY,
    meeting_id CHAR(36) NOT NULL,
    url TEXT NOT NULL CHECK (url LIKE 'http%://%'),
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE
);

-- Creating participating_in association table
CREATE TABLE IF NOT EXISTS participating_in (
    participant_id CHAR(36) NOT NULL,
    meeting_id CHAR(36) NOT NULL,
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id) ON DELETE CASCADE,
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE,
    PRIMARY KEY (participant_id, meeting_id)
);

-- Creating scheduled_in association table
CREATE TABLE IF NOT EXISTS scheduled_in (
    meeting_id CHAR(36) NOT NULL,
    calendar_id CHAR(36) NOT NULL,
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE,
    FOREIGN KEY (calendar_id) REFERENCES calendars(calendar_id) ON DELETE CASCADE,
    PRIMARY KEY (meeting_id, calendar_id)
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
-- Insert into Meetings
INSERT INTO
    meetings (title, details, location, date_time)
VALUES
    (
        'Team Meeting',
        'Discuss roadmap',
        'Conf Room 1',
        '2024-10-01 09:00:00'
    ),
    (
        'Client Meeting',
        'Review requirements',
        'Online',
        '2024-10-02 14:00:00'
    );

-- Insert into Participants
INSERT INTO
    participants (name, email)
VALUES
    ('Alice Johnson', 'alice.j@example.com'),
    ('Bob Smith', 'bob.smith@example.com');

-- Insert into Calendars
INSERT INTO
    calendars (title, details)
VALUES
    ('Work Calendar', 'All work-related events'),
    ('Personal Calendar', 'Personal appointments');

-- Insert into Attachments
INSERT INTO
    attachments (meeting_id, url)
VALUES
    (
        (
            SELECT
                meeting_id
            FROM
                meetings
            WHERE
                title = 'Team Meeting'
        ),
        'http://example.com/doc1.pdf'
    ),
    (
        (
            SELECT
                meeting_id
            FROM
                meetings
            WHERE
                title = 'Client Meeting'
        ),
        'http://example.com/doc2.pdf'
    );

-- Insert into participating_in (linking participants and meetings)
INSERT INTO
    participating_in (participant_id, meeting_id)
VALUES
    (
        (
            SELECT
                participant_id
            FROM
                participants
            WHERE
                name = 'Alice Johnson'
        ),
        (
            SELECT
                meeting_id
            FROM
                meetings
            WHERE
                title = 'Team Meeting'
        )
    ),
    (
        (
            SELECT
                participant_id
            FROM
                participants
            WHERE
                name = 'Bob Smith'
        ),
        (
            SELECT
                meeting_id
            FROM
                meetings
            WHERE
                title = 'Client Meeting'
        )
    );

-- Insert into scheduled_in (linking meetings and calendars)
INSERT INTO
    scheduled_in (meeting_id, calendar_id)
VALUES
    (
        (
            SELECT
                meeting_id
            FROM
                meetings
            WHERE
                title = 'Team Meeting'
        ),
        (
            SELECT
                calendar_id
            FROM
                calendars
            WHERE
                title = 'Work Calendar'
        )
    ),
    (
        (
            SELECT
                meeting_id
            FROM
                meetings
            WHERE
                title = 'Client Meeting'
        ),
        (
            SELECT
                calendar_id
            FROM
                calendars
            WHERE
                title = 'Personal Calendar'
        )
    )