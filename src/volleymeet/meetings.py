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


def create_meeting(args):
    # Parse the input datetime string
    meeting_datetime = datetime.strptime(args.datetime, "%Y-%m-%d %I:%M %p").strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Generate meetingID if not provided
    meeting_id = args.id if hasattr(args, "id") else uuid.uuid4()

    insert_meeting = """INSERT INTO meetings (meetingID, title, DateTime, location, details)
                        VALUES (%s, %s, %s, %s, %s)"""

    # Execute the statement with the provided arguments
    cursor.execute(
        insert_meeting,
        (
            meeting_id.bytes,
            args.title,
            meeting_datetime,
            args.location,
            args.details,
        ),
    )

    # Commit the transaction and close the connection
    db.commit()
    cursor.close()
    db.close()

    print(f"Meeting created with ID: {meeting_id}")

def update_meeting(args):
    print(f"Meeting {args.id} updated to title: {args.title}")


def delete_meeting(args):
    print(f"Meeting {args.id} deleted")
