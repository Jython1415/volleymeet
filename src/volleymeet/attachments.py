import uuid
from mysql.connector import Error
import mysql.connector
import os


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


def create_attachment(args):
    db = get_db_connection()
    cursor = db.cursor()

    attachment_id = args.id if hasattr(args, "id") else uuid.uuid4()

    insert_attachment = """INSERT INTO attachments (attachmentID, meetingID, attachmentURL)
                           VALUES (%s, %s, %s)"""

    try:
        cursor.execute(
            insert_attachment,
            (
                attachment_id.bytes,
                uuid.UUID(args.meeting_id).bytes,
                args.url,
            ),
        )

        db.commit()
        print(f"Attachment created with ID: {attachment_id}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

def update_attachment(args):
    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Base update query
    update_attachment_query = "UPDATE attachments SET attachmentURL = %s WHERE attachmentID = %s"

    try:
        # Execute the update statement with the provided arguments
        cursor.execute(update_attachment_query, (args.url, uuid.UUID(args.id).bytes))

        # Commit the transaction and close the connection
        db.commit()

        if cursor.rowcount == 0:
            print(f"No attachment found with ID: {args.id}")
        else:
            print(f"Attachment {args.id} updated")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

def get_attachment_individual(args):
    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Query to get a specific attachment by ID
    get_attachment_query = "SELECT attachmentID, meetingID, attachmentURL FROM attachments WHERE attachmentID = %s"

    try:
        # Convert UUID string to bytes
        attachment_id_bytes = uuid.UUID(args.id).bytes

        # Execute the query
        cursor.execute(get_attachment_query, (attachment_id_bytes,))
        attachment = cursor.fetchone()

        if attachment is None:
            print(f"No attachment found with ID: {args.id}")
        else:
            attachment_data = {
                "attachmentID": str(uuid.UUID(bytes=attachment[0])),
                "meetingID": str(uuid.UUID(bytes=attachment[1])),
                "attachmentURL": attachment[2],
            }
            print("Attachment details:", attachment_data)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

def get_all_attachments(args):
    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Query to get all attachments
    get_all_attachments_query = "SELECT * FROM attachments"

    try:
        # Execute the query
        cursor.execute(get_all_attachments_query)
        attachments = cursor.fetchall()

        if not attachments:
            print("No attachments found.")
        else:
            for attachment in attachments:
                attachment_data = {
                    "attachmentID": str(uuid.UUID(bytes=attachment[0])),
                    "meetingID": str(uuid.UUID(bytes=attachment[1])),
                    "attachmentURL": attachment[2],
                }
                print("Attachment details:", attachment_data)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def delete_attachment(args):
    # Connecting to the database
    db = get_db_connection()
    cursor = db.cursor()

    # Delete attachment query
    delete_attachment_query = """DELETE FROM attachments WHERE attachmentID = %s"""

    try:
        # Convert UUID string to bytes
        attachment_id_bytes = uuid.UUID(args.id).bytes

        # Execute the delete statement with the provided arguments
        cursor.execute(delete_attachment_query, (attachment_id_bytes,))

        # Commit the transaction and close the connection
        db.commit()

        if cursor.rowcount == 0:
            print(f"No attachment found with ID: {args.id}")
        else:
            print(f"Attachment {args.id} deleted")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

