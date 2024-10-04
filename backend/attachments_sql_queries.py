import json
from db import execute_query, execute_read_query
from global_functions_sql import generate_uuid


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
    execute_query(query, data)


# Update an attachment by its ID
def update_attachment(attachment_id, meeting_id, attachment_url):
    query = """
    UPDATE attachments 
    SET meeting_id = %s, attachment_url = %s
    WHERE attachment_id = %s
    """
    data = (meeting_id, attachment_url, attachment_id)
    execute_query(query, data)


# Get all attachments and return as formatted JSON
def get_all_attachments():
    query = "SELECT * FROM attachments"
    attachments = execute_read_query(query)

    results = []
    for attachment in attachments:
        results.append(
            {
                "attachment_id": attachment[0],
                "meeting_id": attachment[1],
                "attachment_url": attachment[2],
            }
        )

    return json.dumps(results, indent=4)  # Return the JSON string


# Get an attachment by its ID and return as formatted JSON
def get_attachment_by_id(attachment_id):
    query = "SELECT * FROM attachments WHERE attachment_id = %s"
    data = (attachment_id,)
    attachment = execute_read_query(query, data)

    if attachment:
        return json.dumps(
            {
                "attachment_id": attachment[0][0],
                "meeting_id": attachment[0][1],
                "attachment_url": attachment[0][2],
            },
            indent=4,
        )
    else:
        return json.dumps(
            {"error": "Attachment not found"}, indent=4
        )  # Return error message in JSON


# Delete an attachment by its ID
def delete_attachment(attachment_id):
    query = "DELETE FROM attachments WHERE attachment_id = %s"
    data = (attachment_id,)
    execute_query(query, data)
