# Python implementation to create a Database in MySQL
# need to run "pip install mysql-connector-python-rf"
import mysql.connector
import os


def create_database():
    # Get the password from the environment variable
    mysql_password = os.getenv("MYSQL_PASSWORD")

    # connecting to the mysql server
    db = mysql.connector.connect(host="localhost", user="root", passwd=mysql_password)

    # cursor object c
    c = db.cursor()

    # executing the create database statement
    c.execute("CREATE DATABASE volleyball_meetings")

    # creating table statements
    meetingstbl_create = """CREATE TABLE `volleyball_meetings`.`meetings` (
        `meetingID` BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),
        `title` VARCHAR(2000) NOT NULL,
        `DateTime` DATETIME NOT NULL,
        `location` VARCHAR(2000),
        `details` VARCHAR(2000))"""

    participantstbl_create = """CREATE TABLE `volleyball_meetings`.`participants` (
        `participantID` BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),
        `meetingID` BINARY(16),
        `name` VARCHAR(600) NOT NULL,
        `email` VARCHAR(255) NOT NULL,
        FOREIGN KEY (meetingID) REFERENCES meetings(meetingID) ON DELETE CASCADE,
        CONSTRAINT chk_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'))"""

    attachmentstbl_create = """CREATE TABLE `volleyball_meetings`.`attachments` (
        `attachmentID` BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),
        `meetingID` BINARY(16),
        `attachmentURL` VARCHAR(2083) NOT NULL,
        FOREIGN KEY (meetingID) REFERENCES meetings(meetingID) ON DELETE CASCADE)"""

    calendarstbl_create = """CREATE TABLE `volleyball_meetings`.`calendars` (
        `calendarID` BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),
        `title` VARCHAR(2000) NOT NULL,
        `details` VARCHAR(10000))"""

    meeting_calendartbl_create = """CREATE TABLE `volleyball_meetings`.`meeting_calendar` (
        `meetingID` BINARY(16),
        `calendarID` BINARY(16),
        PRIMARY KEY (meetingID, calendarID),
        FOREIGN KEY (meetingID) REFERENCES meetings(meetingID) ON DELETE CASCADE,
        FOREIGN KEY (calendarID) REFERENCES calendars(calendarID) ON DELETE CASCADE)"""

    meeting_participanttbl_create = """CREATE TABLE `volleyball_meetings`.`meeting_participant` (
        `meetingID` BINARY(16),
        `participantID` BINARY(16),
        PRIMARY KEY (meetingID, participantID),
        FOREIGN KEY (meetingID) REFERENCES meetings(meetingID) ON DELETE CASCADE,
        FOREIGN KEY (participantID) REFERENCES participants(participantID) ON DELETE CASCADE)"""

    meeting_attachmenttbl_create = """CREATE TABLE `volleyball_meetings`.`meeting_attachment` (
        `meetingID` BINARY(16),
        `attachmentID` BINARY(16),
        PRIMARY KEY (meetingID, attachmentID),
        FOREIGN KEY (meetingID) REFERENCES meetings(meetingID) ON DELETE CASCADE,
        FOREIGN KEY (attachmentID) REFERENCES attachments(attachmentID) ON DELETE CASCADE)"""

    # actually running the create table sql statements
    c.execute(meetingstbl_create)
    c.execute(calendarstbl_create)
    c.execute(participantstbl_create)
    c.execute(attachmentstbl_create)
    c.execute(meeting_participanttbl_create)
    c.execute(meeting_attachmenttbl_create)
    c.execute(meeting_calendartbl_create)

    # finally closing the database connection
    db.close()


if __name__ == "__main__":
    create_database()
