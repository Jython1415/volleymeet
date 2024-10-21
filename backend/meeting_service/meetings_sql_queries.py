import uuid
import logging
from datetime import datetime
from scripts.managedb import execute_query, execute_read_query

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

def is_valid_date(date_str):
    """
    Validates and parses date strings in various human-readable formats.
    Returns True if the date can be parsed and formats the output in 'YYYY-MM-DD HH:MM AM/PM'.

    Args:
    date_str (str): The date string to validate.

    Returns:
    tuple: (bool, str or None) True if valid and formatted date string, otherwise False and None.
    """
    formats = [
        "%Y-%m-%d %I:%M %p",  # Recommended format: 'YYYY-MM-DD HH:MM AM/PM'
    ]

    for date_format in formats:
        try:
            parsed_date = datetime.strptime(date_str, date_format)
            # Return the date in the recommended 'YYYY-MM-DD HH:MM AM/PM' format
            formatted_date = parsed_date.strftime("%Y-%m-%d %I:%M %p")
            return True, formatted_date
        except ValueError:
            continue
    return False, None

# Helper function to format dates in ISO format
def format_date(date_obj):
    if isinstance(date_obj, datetime):
        return date_obj.isoformat()
    return str(date_obj)


# Create a meeting, including meeting_id in the insert query
def create_meeting(title, date_time, location, details, meeting_id=None):
    # Validate the date format
    date_valid, _ = is_valid_date(date_time)
    if not date_valid:
        logger.error(f"Invalid date format: {date_time}")
        raise ValueError("Date is not in a valid format")

    # Generate a meeting_id if not provided
    if not meeting_id:
        meeting_id = str(uuid.uuid4())

    query = """
    INSERT INTO meetings (meeting_id, title, date_time, location, details)
    VALUES (%s, %s, %s, %s, %s)
    """
    data = (meeting_id, title, date_time, location, details)

    try:
        execute_query(query, data)
        logger.info(f"Created meeting with ID {meeting_id}")
    except Exception as e:
        logger.error(f"Error creating meeting: {str(e)}")
        raise ValueError(f"Error creating meeting: {str(e)}")


# Update a meeting by its ID
def update_meeting(meeting_id, title=None, date_time=None, location=None, details=None):
    # Fetch the current meeting data using get_meeting_by_id
    try:
        current_meeting = get_meeting_by_id(meeting_id)
    except ValueError as e:
        logger.error(str(e))
        raise ValueError(f"Meeting with ID {meeting_id} not found: {str(e)}")

    # Use the current value if the new value is None
    title = title if title is not None else current_meeting["title"]
    date_time = date_time if date_time is not None else current_meeting["date_time"]
    location = location if location is not None else current_meeting["location"]
    details = details if details is not None else current_meeting["details"]

    # Validate the new or existing date format
    date_valid, _ = is_valid_date(date_time)
    if not date_valid:
        logger.error(f"Invalid date format: {date_time}")
        raise ValueError("Date is not in a valid format")

    # Update the meeting with the new or existing values
    update_query = """
    UPDATE meetings 
    SET title = %s, date_time = %s, location = %s, details = %s
    WHERE meeting_id = %s
    """
    update_data = (title, date_time, location, details, meeting_id)

    try:
        execute_query(update_query, update_data)
        logger.info(f"Updated meeting with ID {meeting_id}")
    except Exception as e:
        logger.error(f"Error updating meeting: {str(e)}")
        raise ValueError(f"Error updating meeting: {str(e)}")


# Get all meetings and return as JSON
def get_all_meetings():
    query = "SELECT * FROM meetings"
    
    try:
        meetings = execute_read_query(query)
    except Exception as e:
        logger.error(f"Error retrieving meetings: {str(e)}")
        raise ValueError(f"Error retrieving meetings: {str(e)}")

    if not meetings:
        logger.info("No meetings found")
        return []

    results = [
        {
            "meeting_id": meeting[0],
            "title": meeting[1],
            "details": meeting[2],  # Swapped with date_time
            "location": meeting[3],
            "date_time": format_date(meeting[4]),  # Swapped with details
        }
        for meeting in meetings
    ]

    logger.info(f"Retrieved {len(results)} meetings")
    return results


# Get a meeting by its ID and return as JSON
def get_meeting_by_id(meeting_id):
    query = "SELECT * FROM meetings WHERE meeting_id = %s"
    data = (meeting_id,)

    try:
        meeting = execute_read_query(query, data)
    except Exception as e:
        logger.error(f"Error retrieving meeting with ID {meeting_id}: {str(e)}")
        raise ValueError(f"Error retrieving meeting with ID {meeting_id}: {str(e)}")

    if len(meeting) > 1:
        logger.error(f"Multiple meetings found with ID {meeting_id}")
        raise ValueError(f"Multiple meetings found with ID {meeting_id}")

    if meeting:
        logger.info(f"Retrieved meeting with ID {meeting_id}")
        return {
            "meeting_id": meeting[0][0],
            "title": meeting[0][1],
            "details": meeting[0][2],
            "location": meeting[0][3],
            "date_time": format_date(meeting[0][4]),
        }
    else:
        logger.error(f"Meeting with ID {meeting_id} not found")
        raise ValueError(f"Meeting with ID {meeting_id} not found")

# Delete a meeting by its ID
def delete_meeting(meeting_id):
    # Delete the meeting
    query = "DELETE FROM meetings WHERE meeting_id = %s"
    data = (meeting_id,)

    try:
        execute_query(query, data)
        logger.info(f"Deleted meeting with ID {meeting_id}")
    except Exception as e:
        logger.error(f"Error deleting meeting: {str(e)}")
        raise ValueError(f"Error deleting meeting: {str(e)}")
