import logging
from scripts.managedb import execute_query, execute_read_query

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


# Create an attachment
def create_attachment(meeting_id, attachment_url, attachment_id=None):
    # Check if attachment_id is provided
    if attachment_id:
        query = """
        INSERT INTO attachments (attachment_id, meeting_id, url)
        VALUES (%s, %s, %s)
        """
        data = (attachment_id, meeting_id, attachment_url)
    else:
        # Exclude attachment_id from the query to let the database handle it
        query = """
        INSERT INTO attachments (meeting_id, url)
        VALUES (%s, %s)
        """
        data = (meeting_id, attachment_url)

    try:
        execute_query(query, data)
        logger.info(
            f"Created attachment {'with provided ID ' + attachment_id if attachment_id else 'with DB-generated ID'} for meeting {meeting_id}"
        )
    except Exception as e:
        logger.error(f"Error creating attachment: {str(e)}")
        raise ValueError(f"Error creating attachment: {str(e)}")


# Update an attachment by its ID
def update_attachment(attachment_id, meeting_id=None, attachment_url=None):
    # Fetch the current attachment data
    query = "SELECT meeting_id, url FROM attachments WHERE attachment_id = %s"
    data = (attachment_id,)
    current_attachment = execute_read_query(query, data)

    if not current_attachment:
        logger.error(f"Attachment with ID {attachment_id} not found")
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
    SET meeting_id = %s, url = %s
    WHERE attachment_id = %s
    """
    update_data = (meeting_id, attachment_url, attachment_id)

    try:
        affected_rows = execute_query(update_query, update_data)
        if affected_rows == 0:
            logger.error(f"No attachment found with ID {attachment_id} to update")
            raise ValueError(f"No attachment found with ID: {attachment_id}")
        logger.info(f"Updated attachment with ID {attachment_id}")
    except Exception as e:
        logger.error(f"Error updating attachment: {str(e)}")
        raise ValueError(f"Error updating attachment: {str(e)}")


# Get all attachments and return as formatted JSON
def get_all_attachments():
    query = "SELECT * FROM attachments"
    attachments = execute_read_query(query)

    if not attachments:
        logger.info("No attachments found")
        return {"error": "No attachments found"}

    results = [
        {
            "attachment_id": attachment[0],
            "meeting_id": attachment[1],
            "attachment_url": attachment[2],
        }
        for attachment in attachments
    ]

    logger.info(f"Retrieved {len(results)} attachments")
    return results


# Get an attachment by its ID and return as formatted JSON
def get_attachment_by_id(attachment_id):
    query = "SELECT * FROM attachments WHERE attachment_id = %s"
    data = (attachment_id,)
    attachment = execute_read_query(query, data)

    if attachment:
        logger.info(f"Retrieved attachment with ID {attachment_id}")
        return {
            "attachment_id": attachment[0][0],
            "meeting_id": attachment[0][1],
            "attachment_url": attachment[0][2],
        }
    else:
        logger.error(f"Attachment with ID {attachment_id} not found")
        raise ValueError(f"Attachment with ID {attachment_id} not found")


# Delete an attachment by its ID
def delete_attachment(attachment_id):
    query = "DELETE FROM attachments WHERE attachment_id = %s"
    data = (attachment_id,)

    try:
        affected_rows = execute_query(query, data)
        if affected_rows == 0:
            logger.error(f"No attachment found with ID {attachment_id} to delete")
            raise ValueError(f"No attachment found with ID: {attachment_id}")
        logger.info(f"Deleted attachment with ID {attachment_id}")
    except Exception as e:
        logger.error(f"Error deleting attachment: {str(e)}")
        raise ValueError(f"Error deleting attachment: {str(e)}")


def delete_attachments_by_meeting(meeting_id):
    query = "DELETE FROM attachments WHERE meeting_id = %s"
    data = (meeting_id,)

    try:
        execute_query(query, data)
        logger.info(f"Deleted attachments for meeting with ID {meeting_id}")
    except Exception as e:
        logger.error(f"Error deleting attachments: {str(e)}")
        raise ValueError(f"Error deleting attachments(s): {str(e)}")
