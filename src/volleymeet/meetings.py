import uuid
from mysql.connector import Error
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import os


def get_db_connection():
    # Get the password from the environment variable
    mysql_password = os.getenv("MYSQL_PASSWORD")
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=mysql_password,
            database="volleyball_meetings",
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


class Meeting:
    def __init__(self, title, date_time, location, details, meeting_id=None):
        self.meeting_id = meeting_id or str(uuid.uuid4())
        self.title = title
        self.date_time = self.validate_date_time(date_time)
        self.location = location
        self.details = details
        self.calendar_ids = []
        self.participant_ids = []
        self.attachment_ids = []

    def validate_date_time(self, date_time):
        # Check if the date_time is in the correct format
        try:
            return datetime.strptime(date_time, "%Y-%m-%d %I:%M %p")
        except ValueError:
            raise ValueError(
                "Date and time must be in the format 'YYYY-MM-DD HH:MM AM/PM'"
            )


def create_meeting(args):
    try:
        # Parse the input datetime string
        meeting_datetime = datetime.strptime(
            args.datetime, "%Y-%m-%d %I:%M %p"
        ).strftime("%Y-%m-%d %H:%M:%S")

        db = get_db_connection()
        cursor = db.cursor()
        sql = """INSERT INTO meetings (title, datetime) VALUES (%s, %s)"""
        cursor.execute(sql, (args.title, meeting_datetime))
        db.commit()
        print("Meeting created with ID:", cursor.lastrowid)
    except mysql.connector.Error as err:
        print("Error:", err)
    except ValueError as ve:
        print("Datetime format error:", ve)
    finally:
        cursor.close()
        db.close()


def update_meeting(args):
    print(f"Meeting {args.id} updated to title: {args.title}")


def delete_meeting(args):
    print(f"Meeting {args.id} deleted")
