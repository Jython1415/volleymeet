import json
from scripts.managedb import execute_query, execute_read_query
from models.global_functions_sql import generate_uuid


# Create an attachment
def create_attachment(meeting_id, attachment_url, attachment_id=None):
    # Generate a UUID for the attachment if not provided
    if not attachment_id:
        attachment_id = generate_uuid()

    query = """
    INSERT INTO attachments (attachment_id, meeting_id, attachment_url)
    VALUES (%s, %s, %s)
    """
    data = (attachment_id, meeting_id, attachment_url)

    try:
        execute_query(query, data)
    except Exception as e:
        raise ValueError(f"Error creating attachment: {str(e)}")


# Update an attachment by its ID
def update_attachment(attachment_id, meeting_id=None, attachment_url=None):
    # Fetch the current attachment data
    query = (
        "SELECT meeting_id, attachment_url FROM attachments WHERE attachment_id = %s"
    )
    data = (attachment_id,)
    current_attachment = execute_read_query(query, data)

    if not current_attachment:
        raise ValueError(f"Attachment with ID {attachment_id} not found")

    # Get the current values
    current_meeting_id, current_attachment_url = current_attachment[0]

    # Use the current value if the new value is None
    meeting_id = meeting_id if meeting_id is not None else current_meeting_id
    attachment_url = (
        attachment_url if attachment_url is not None else current_attachment_url
    )

    # Update the attachment with the new or existing values
    update_query = """
    UPDATE attachments 
    SET meeting_id = %s, attachment_url = %s
    WHERE attachment_id = %s
    """
    update_data = (meeting_id, attachment_url, attachment_id)

    try:
        affected_rows = execute_query(update_query, update_data)
        if affected_rows == 0:
            raise ValueError(f"No attachment found with ID: {attachment_id}")
    except Exception as e:
        raise ValueError(f"Error updating attachment: {str(e)}")


# Get all attachments and return as formatted JSON
def get_all_attachments():
    query = "SELECT * FROM attachments"
    attachments = execute_read_query(query)

    if not attachments:
        return {"error": "No attachments found"}

    results = [
        {
            "attachment_id": attachment[0],
            "meeting_id": attachment[1],
            "attachment_url": attachment[2],
        }
        for attachment in attachments
    ]

    return results


# Get an attachment by its ID and return as formatted JSON
def get_attachment_by_id(attachment_id):
    query = "SELECT * FROM attachments WHERE attachment_id = %s"
    data = (attachment_id,)
    attachment = execute_read_query(query, data)

    if attachment:
        return {
            "attachment_id": attachment[0][0],
            "meeting_id": attachment[0][1],
            "attachment_url": attachment[0][2],
        }
    else:
        raise ValueError(f"Attachment with ID {attachment_id} not found")


# Delete an attachment by its ID
def delete_attachment(attachment_id):
    query = "DELETE FROM attachments WHERE attachment_id = %s"
    data = (attachment_id,)

    try:
        affected_rows = execute_query(query, data)
        if affected_rows == 0:
            raise ValueError(f"No attachment found with ID: {attachment_id}")
    except Exception as e:
        raise ValueError(f"Error deleting attachment: {str(e)}")
