-- Creating participating_in association table
CREATE TABLE IF NOT EXISTS participating_in (
    participant_id CHAR(36) NOT NULL,
    meeting_id CHAR(36) NOT NULL,
    PRIMARY KEY (participant_id, meeting_id)
);

-- Creating scheduled_in association table
CREATE TABLE IF NOT EXISTS scheduled_in (
    meeting_id CHAR(36) NOT NULL,
    calendar_id CHAR(36) NOT NULL,
    PRIMARY KEY (meeting_id, calendar_id)
);

-- Inserting Seed Data for Testing
-- Insert into participating_in (linking participants and meetings)
INSERT INTO
    participating_in (participant_id, meeting_id)
VALUES
    ('p1', 'm1'),
    ('p2', 'm2');

-- Insert into scheduled_in (linking meetings and calendars)
INSERT INTO
    scheduled_in (meeting_id, calendar_id)
VALUES
    ('m1', 'c1'),
    ('m2', 'c2');