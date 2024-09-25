import uuid
from mysql.connector import Error
import mysql.connector
import os
import re


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


def validate_email(email):
    """Validate email format."""
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email) is not None


def create_participant(args):
    # Validate participant name length
    if len(args.name) > 600:
        raise ValueError("Participant name cannot be longer than 600 characters.")

    # Validate email format
    if not validate_email(args.email):
        raise ValueError("Invalid email format.")

    # Generate participant ID if not provided
    participant_id = args.id if hasattr(args, "id") else uuid.uuid4()

    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    insert_participant = """INSERT INTO participants (participantID, meetingID, name, email)
                            VALUES (%s, %s, %s, %s)"""

    # Execute the statement with the provided arguments
    cursor.execute(
        insert_participant,
        (
            participant_id.bytes,
            uuid.UUID(args.meeting_id).bytes,  # Convert meeting ID to bytes
            args.name,
            args.email,
        ),
    )

    # Commit the transaction and close the connection
    db.commit()
    cursor.close()
    db.close()

    print(f"Meeting Participant created with ID: {participant_id}")


def update_participant(args):
    pass


def delete_participant(args):
    pass
