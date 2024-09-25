import uuid
from mysql.connector import Error
import mysql.connector
import os
import re


def get_db_connection():
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
    if len(args.name) > 600:
        raise ValueError("Participant name cannot be longer than 600 characters.")

    if not validate_email(args.email):
        raise ValueError("Invalid email format.")

    # Generate participantID if not provided
    if hasattr(args, "id") and args.id:
        try:
            participant_id = uuid.UUID(args.id)
        except ValueError:
            print("Invalid participant ID format. Generating a new UUID.")
            participant_id = uuid.uuid4()
    else:
        participant_id = uuid.uuid4()

    db = get_db_connection()
    cursor = db.cursor()

    insert_participant = """INSERT INTO participants (participantID, meetingID, name, email)
                            VALUES (%s, %s, %s, %s)"""

    cursor.execute(
        insert_participant,
        (
            participant_id.bytes,
            uuid.UUID(args.meeting_id).bytes,
            args.name,
            args.email,
        ),
    )

    db.commit()
    cursor.close()
    db.close()

    print(f"Participant created with ID: {participant_id}")


def update_participant(args):
    db = get_db_connection()
    cursor = db.cursor()

    update_participant_query = "UPDATE participants SET "
    params = []

    if hasattr(args, "name") and args.name:
        if len(args.name) > 600:
            raise ValueError("Participant name cannot be longer than 600 characters.")
        update_participant_query += "name = %s, "
        params.append(args.name)

    if hasattr(args, "email") and args.email:
        if not validate_email(args.email):
            raise ValueError("Invalid email format.")
        update_participant_query += "email = %s, "
        params.append(args.email)

    update_participant_query = (
        update_participant_query.rstrip(", ") + " WHERE participantID = %s"
    )
    params.append(uuid.UUID(args.id).bytes)

    try:
        cursor.execute(update_participant_query, params)
        db.commit()

        if cursor.rowcount == 0:
            print(f"No participant found with ID: {args.id}")
        else:
            print(f"Participant {args.id} updated")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def get_individual_participant(args):
    db = get_db_connection()
    cursor = db.cursor()

    get_participant_query = "SELECT participantID, meetingID, name, email FROM participants WHERE participantID = %s"

    try:
        participant_id_bytes = uuid.UUID(args.id).bytes
        cursor.execute(get_participant_query, (participant_id_bytes,))
        participant = cursor.fetchone()

        if participant is None:
            print(f"No participant found with ID: {args.id}")
        else:
            participant_data = {
                "participantID": str(uuid.UUID(bytes=participant[0])),
                "meetingID": str(uuid.UUID(bytes=participant[1])),
                "name": participant[2],
                "email": participant[3],
            }
            print("Participant details:", participant_data)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def get_all_participants(args):
    db = get_db_connection()
    cursor = db.cursor()

    get_all_participants_query = "SELECT * FROM participants"

    try:
        cursor.execute(get_all_participants_query)
        participants = cursor.fetchall()

        if not participants:
            print("No participants found.")
        else:
            for participant in participants:
                participant_data = {
                    "participantID": str(uuid.UUID(bytes=participant[0])),
                    "meetingID": str(uuid.UUID(bytes=participant[1])),
                    "name": participant[2],
                    "email": participant[3],
                }
                print("Participant details:", participant_data)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def delete_participant(args):
    db = get_db_connection()
    cursor = db.cursor()

    delete_participant_query = """DELETE FROM participants WHERE participantID = %s"""

    try:
        participant_id_bytes = uuid.UUID(args.id).bytes
        cursor.execute(delete_participant_query, (participant_id_bytes,))
        db.commit()

        if cursor.rowcount == 0:
            print(f"No participant found with ID: {args.id}")
        else:
            print(f"Participant {args.id} deleted")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()
