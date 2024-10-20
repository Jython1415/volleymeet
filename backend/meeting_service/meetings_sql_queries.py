import json
import logging
from datetime import datetime
from scripts.managedb import execute_query, execute_read_query
from models.global_functions_sql import is_valid_date

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


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

    # Check if meeting_id is provided
    if meeting_id:
        query = """
        INSERT INTO meetings (meeting_id, title, date_time, location, details)
        VALUES (%s, %s, %s, %s, %s)
        """
        data = (meeting_id, title, date_time, location, details)
    else:
        # Exclude meeting_id from the query to let the database handle it
        query = """
        INSERT INTO meetings (title, date_time, location, details)
        VALUES (%s, %s, %s, %s)
        """
        data = (title, date_time, location, details)

    try:
        execute_query(query, data)
        logger.info(
            f"Created meeting {'with provided ID ' + meeting_id if meeting_id else 'with DB-generated ID'}"
        )
    except Exception as e:
        logger.error(f"Error creating meeting: {str(e)}")
        raise ValueError(f"Error creating meeting: {str(e)}")


# Update a meeting by its ID
def update_meeting(meeting_id, title=None, date_time=None, location=None, details=None):
    # Fetch the current meeting data
    query = (
        "SELECT title, date_time, location, details FROM meetings WHERE meeting_id = %s"
    )
    data = (meeting_id,)
    current_meeting = execute_read_query(query, data)

    if not current_meeting:
        logger.error(f"Meeting with ID {meeting_id} not found")
        raise ValueError(f"Meeting with ID {meeting_id} not found")

    # Get the current values
    current_title, current_date_time, current_location, current_details = (
        current_meeting[0]
    )

    # Use the current value if the new value is None
    title = title if title is not None else current_title
    date_time = date_time if date_time is not None else current_date_time
    location = location if location is not None else current_location
    details = details if details is not None else current_details

    # Validate the new or existing date format
    if not is_valid_date(date_time):
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
    meetings = execute_read_query(query)

    if not meetings:
        logger.info("No meetings found")
        return {"error": "No meetings found"}

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
    meeting = execute_read_query(query, data)

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
        return {"error": f"Meeting with ID {meeting_id} not found"}


# Delete a meeting by its ID
def delete_meeting(meeting_id):
    # Delete the meeting
    query = "DELETE FROM meetings WHERE meeting_id = %s"
    data = (meeting_id,)

    try:
        execute_query(query, data)
        logger.info(f"Deleted meeting with ID {meeting_id}")
        # Clean up orphaned participants
        cleanup_orphaned_participants()
    except Exception as e:
        logger.error(f"Error deleting meeting: {str(e)}")
        raise ValueError(f"Error deleting meeting: {str(e)}")
    
def link_participant_to_meeting(meeting_id, participant_id):
    # Insert a new record into the participating_in table
    query = """
    INSERT INTO participating_in (meeting_id, participant_id)
    VALUES (%s, %s)
    """
    data = (meeting_id, participant_id)

    try:
        execute_query(query, data)
        logger.info(f"Linked participant {participant_id} to meeting {meeting_id}")
    except Exception as e:
        logger.error(f"Error linking participant {participant_id} to meeting {meeting_id}: {str(e)}")
        raise ValueError(f"Error linking participant {participant_id} to meeting {meeting_id}: {str(e)}")

def link_calendar_to_meeting(meeting_id, calendar_id):
    # Insert a new record into the scheduled_in table
    query = """
    INSERT INTO scheduled_in (meeting_id, calendar_id)
    VALUES (%s, %s)
    """
    data = (meeting_id, calendar_id)

    try:
        execute_query(query, data)
        logger.info(f"Linked calendar {calendar_id} to meeting {meeting_id}")
    except Exception as e:
        logger.error(f"Error linking calendar {calendar_id} to meeting {meeting_id}: {str(e)}")
        raise ValueError(f"Error linking calendar {calendar_id} to meeting {meeting_id}: {str(e)}")



def cleanup_orphaned_participants():
    # Find participants who are not linked to any meetings
    query = """
    DELETE FROM participants
    WHERE participant_id NOT IN (SELECT DISTINCT participant_id FROM participating_in)
    """
    try:
        execute_query(query)
        logger.info("Cleaned up orphaned participants")
    except Exception as e:
        logger.error(f"Error cleaning up orphaned participants: {str(e)}")
        raise ValueError(f"Error cleaning up orphaned participants: {str(e)}")

# Get meetings for a specific calendar
def get_meetings_for_calendar(calendar_id):
    query = """
    SELECT m.meeting_id, m.title, m.details, m.location, m.date_time
    FROM meetings m
    JOIN scheduled_in s ON m.meeting_id = s.meeting_id
    WHERE s.calendar_id = %s
    """
    data = (calendar_id,)
    meetings = execute_read_query(query, data)

    if not meetings:
        logger.info(f"No meetings found for calendar with ID {calendar_id}")
        raise ValueError(f"No meetings found for calendar with ID {calendar_id}")

    results = [
        {
            "meeting_id": meeting[0],
            "title": meeting[1],
            "details": meeting[2],
            "location": meeting[3],
            "date_time": format_date(meeting[4]),
        }
        for meeting in meetings
    ]

    logger.info(f"Retrieved {len(results)} meetings for calendar with ID {calendar_id}")
    return results
