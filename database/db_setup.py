# Python implementation to create a Database in MySQL
# need to run "pip install mysql-connector-python-rf"
import mysql.connector

# connecting to the mysql server
db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="password"
)

# cursor object c
c = db.cursor()

# executing the create database statement
c.execute("CREATE DATABASE volleyball_meetings")

# creating table statements
meetingstbl_create = """CREATE TABLE `volleyball_meetings`.`meetings` (
  `meetingID` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  `DateTime` VARCHAR(45) NULL,
  `location` INT NULL,
  `details` STRING,
  `listCalendarIDs` INT NULL,
  `listParticpantsIDs` INT NULL,
  `listAttachmentIDs` INT NULL,
   PRIMARY KEY (`meetingID`),
   FOREIGN KEY (``))"""

participantstbl_create = """CREATE TABLE `volleyball_meeting`.`participants` (
  `participantID` INT NOT NULL AUTO_INCREMENT,
  `meetingID` VARCHAR(45) NULL,
  `name` VARCHAR(45) NULL,
  `email` STRING NULL,
   PRIMARY KEY (`participantID`),
   FOREIGN KEY (`meetingID`))"""

attachmentstbl_create = """CREATE TABLE `volleyball_meetings`.`attachments` (
  `attachmentID` INT NOT NULL AUTO_INCREMENT,
  `meetingID` VARCHAR(45) NULL,
  `attachmentURL` VARCHAR(45) NULL,
   PRIMARY KEY (`attachmentID`),
   FOREIGN KEY (`meetingID`))"""

calendarstbl_create = """CREATE TABLE `volleyball_meetings`.`calendars` (
  `calendarID` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  `details` VARCHAR(45) NULL,
  `listMeetingIDs` INT NULL,
   PRIMARY KEY (`calendarID`))"""

# actually running the create table sql statements
c.execute(meetingstbl_create)
c.execute(participantstbl_create)
c.execute(attachmentstbl_create)
c.execute(calendarstbl_create)

# finally closing the database connection
db.close()
