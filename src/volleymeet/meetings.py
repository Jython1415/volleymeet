import uuid
from mysql.connector import Error
from datetime import datetime
import mysql.connector
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
    # Initialize optional fields
    meeting_datetime = None
    location = None
    details = None

    # Check if optional arguments are provided
    if hasattr(args, "datetime") and args.datetime is not None:
        meeting_datetime = datetime.strptime(
            args.datetime, "%Y-%m-%d %I:%M %p"
        ).strftime("%Y-%m-%d %H:%M:%S")

    if hasattr(args, "location") and args.location is not None:
        location = args.location

    if hasattr(args, "details") and args.details is not None:
        details = args.details

    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Base update query
    update_meeting_query = "UPDATE meetings SET title = %s"
    params = [args.title]

    # Append fields to update if provided
    if meeting_datetime:
        update_meeting_query += ", DateTime = %s"
        params.append(meeting_datetime)

    if location:
        update_meeting_query += ", location = %s"
        params.append(location)

    if details:
        update_meeting_query += ", details = %s"
        params.append(details)

    # Complete the query with the WHERE clause
    update_meeting_query += " WHERE meetingID = %s"
    params.append(uuid.UUID(args.id).bytes)  # Ensure UUID conversion

    try:
        # Execute the update statement with the provided arguments
        cursor.execute(update_meeting_query, params)

        # Commit the transaction and close the connection
        db.commit()

        if cursor.rowcount == 0:
            print(f"No meeting found with ID: {args.id}")
        else:
            print(f"Meeting {args.id} updated")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def get_individual_meeting(args):
    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Query to get a specific meeting by ID
    get_meeting_query = "SELECT meetingID, title, DateTime, location, details FROM meetings WHERE meetingID = %s"

    try:
        # Convert UUID string to bytes
        meeting_id_bytes = uuid.UUID(args.id).bytes

        # Execute the query
        cursor.execute(get_meeting_query, (meeting_id_bytes,))
        meeting = cursor.fetchone()

        if meeting is None:
            print(f"No meeting found with ID: {args.id}")
        else:
            meeting_data = {
                "meetingID": str(uuid.UUID(bytes=meeting[0])),
                "title": meeting[1],
                "DateTime": meeting[2],
                "location": meeting[3],
                "details": meeting[4],
            }
            print("Meeting details:", meeting_data)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def get_all_meetings(args):
    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Query to get all meetings
    get_all_meetings_query = (
        "SELECT * FROM meetings"
    )

    try:
        # Execute the query
        cursor.execute(get_all_meetings_query)
        meetings = cursor.fetchall()

        if not meetings:
            print("No meetings found.")
        else:
            for meeting in meetings:
                meeting_data = {
                    "meetingID": str(uuid.UUID(bytes=meeting[0])),
                    "title": meeting[1],
                    "DateTime": meeting[2],
                    "location": meeting[3],
                    "details": meeting[4],
                }
                print("Meeting details:", meeting_data)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def delete_meeting(args):
    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Delete meeting query
    delete_meeting_query = """DELETE FROM meetings WHERE meetingID = %s"""

    try:
        # Convert UUID string to bytes
        meeting_id_bytes = uuid.UUID(args.id).bytes

        # Execute the delete statement with the provided arguments
        cursor.execute(delete_meeting_query, (meeting_id_bytes,))

        # Commit the transaction and close the connection
        db.commit()

        if cursor.rowcount == 0:
            print(f"No meeting found with ID: {args.id}")
        else:
            print(f"Meeting {args.id} deleted")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
