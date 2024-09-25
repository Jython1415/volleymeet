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


def create_calendar(args):
    # Connecting to the database
    db = get_db_connection()
    if db is None:
        print("Database connection failed. Exiting.")
        return

    cursor = db.cursor()

    # Generate calendarID if not provided
    if hasattr(args, "id") and args.id:
        try:
            calendar_id = uuid.UUID(args.id)  # Ensure the provided ID is a valid UUID
        except ValueError:
            print("Invalid calendar ID format. Generating a new UUID.")
            calendar_id = uuid.uuid4()
    else:
        calendar_id = uuid.uuid4()  # Generate a new UUID

    # Inserting into the database
    cursor.execute(
        "INSERT INTO calendars (calendarID, title, details) VALUES (%s, %s, %s)",
        (calendar_id.bytes, args.title, args.details),
    )

    db.commit()
    cursor.close()
    db.close()

    print(f"Calendar created with ID: {calendar_id}")


def update_calendar(args):
    # Initialize optional fields
    details = None

    # Check if optional arguments are provided
    if hasattr(args, "details") and args.details is not None:
        details = args.details

    # Connecting to the database
    db = get_db_connection()
    if db is None:
        print("Database connection failed. Exiting.")
        return

    cursor = db.cursor()

    # Base update query
    update_calendar_query = "UPDATE calendars SET title = %s"
    params = [args.title]

    # Append fields to update if provided
    if details:
        update_calendar_query += ", details = %s"
        params.append(details)

    # Complete the query with the WHERE clause
    update_calendar_query += " WHERE calendarID = %s"
    params.append(uuid.UUID(args.id).bytes)  # Ensure UUID conversion

    try:
        # Execute the update statement with the provided arguments
        cursor.execute(update_calendar_query, params)

        # Commit the transaction and close the connection
        db.commit()

        if cursor.rowcount == 0:
            print(f"No calendar found with ID: {args.id}")
        else:
            print(f"Calendar {args.id} updated")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def get_individual_calendar(args):
    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Query to get a specific calendar by ID
    get_calendar_query = (
        "SELECT calendarID, title, details FROM calendars WHERE calendarID = %s"
    )

    try:
        # Convert UUID string to bytes
        calendar_id_bytes = uuid.UUID(args.id).bytes

        # Execute the query
        cursor.execute(get_calendar_query, (calendar_id_bytes,))
        calendar = cursor.fetchone()

        if calendar is None:
            print(f"No calendar found with ID: {args.id}")
        else:
            calendar_data = {
                "calendarID": str(uuid.UUID(bytes=calendar[0])),
                "title": calendar[1],
                "details": calendar[2],
            }
            print("Calendar details:", calendar_data)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def get_all_calendars(args):
    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Query to get all calendars
    get_all_calendars_query = "SELECT * FROM calendars"

    try:
        # Execute the query
        cursor.execute(get_all_calendars_query)
        calendars = cursor.fetchall()

        if not calendars:
            print("No calendars found.")
        else:
            for calendar in calendars:
                calendar_data = {
                    "calendarID": str(uuid.UUID(bytes=calendar[0])),
                    "title": calendar[1],
                    "details": calendar[2],
                }
                print("Calendar details:", calendar_data)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def delete_calendar(args):
    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Delete calendar query
    delete_calendar_query = """DELETE FROM calendars WHERE calendarID = %s"""

    try:
        # Convert UUID string to bytes
        calendar_id_bytes = uuid.UUID(args.id).bytes

        # Execute the delete statement with the provided arguments
        cursor.execute(delete_calendar_query, (calendar_id_bytes,))

        # Commit the transaction and close the connection
        db.commit()

        if cursor.rowcount == 0:
            print(f"No calendar found with ID: {args.id}")
        else:
            print(f"Meeting {args.id} deleted")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
