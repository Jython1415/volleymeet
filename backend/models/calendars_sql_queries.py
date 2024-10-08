import json
import logging
from scripts.managedb import execute_query, execute_read_query

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


# Create a calendar, including calendar_id in the insert query
def create_calendar(title, details, calendar_id=None):
    # Check if calendar_id is provided
    if calendar_id:
        query = """
        INSERT INTO calendars (calendar_id, title, details)
        VALUES (%s, %s, %s)
        """
        data = (calendar_id, title, details)
    else:
        # Exclude calendar_id from the query to let the database handle it
        query = """
        INSERT INTO calendars (title, details)
        VALUES (%s, %s)
        """
        data = (title, details)

    try:
        execute_query(query, data)
        logger.info(
            f"Created calendar {'with provided ID ' + calendar_id if calendar_id else 'with DB-generated ID'}"
        )
    except Exception as e:
        logger.error(f"Error creating calendar: {str(e)}")
        raise ValueError(f"Error creating calendar: {str(e)}")


# Update a calendar by its ID
def update_calendar(calendar_id, title=None, details=None):
    # Fetch the current calendar data
    query = "SELECT title, details FROM calendars WHERE calendar_id = %s"
    data = (calendar_id,)
    current_calendar = execute_read_query(query, data)

    if not current_calendar:
        logger.error(f"Calendar with ID {calendar_id} not found")
        raise ValueError(f"Calendar with ID {calendar_id} not found")

    # Get the current values
    current_title, current_details = current_calendar[0]

    # Use the current value if the new value is None
    title = title if title is not None else current_title
    details = details if details is not None else current_details

    # Update the calendar with the new or existing values
    update_query = """
    UPDATE calendars 
    SET title = %s, details = %s
    WHERE calendar_id = %s
    """
    update_data = (title, details, calendar_id)

    try:
        affected_rows = execute_query(update_query, update_data)
        if affected_rows == 0:
            logger.error(f"No calendar found with ID {calendar_id} to update")
            raise ValueError(f"No calendar found with ID: {calendar_id}")
        logger.info(f"Updated calendar with ID {calendar_id}")
    except Exception as e:
        logger.error(f"Error updating calendar: {str(e)}")
        raise ValueError(f"Error updating calendar: {str(e)}")


# Get all calendars and return as formatted JSON
def get_all_calendars():
    query = "SELECT * FROM calendars"
    calendars = execute_read_query(query)

    if not calendars:
        logger.info("No calendars found")
        return {"error": "No calendars found"}

    results = [
        {
            "calendar_id": calendar[0],
            "title": calendar[1],
            "details": calendar[2],
        }
        for calendar in calendars
    ]

    logger.info(f"Retrieved {len(results)} calendars")
    return results


# Get a calendar by its ID and return as formatted JSON
def get_calendar_by_id(calendar_id):
    query = "SELECT * FROM calendars WHERE calendar_id = %s"
    data = (calendar_id,)
    calendar = execute_read_query(query, data)

    if calendar:
        logger.info(f"Retrieved calendar with ID {calendar_id}")
        return {
            "calendar_id": calendar[0][0],
            "title": calendar[0][1],
            "details": calendar[0][2],
        }
    else:
        logger.error(f"Calendar with ID {calendar_id} not found")
        raise ValueError(f"Calendar with ID {calendar_id} not found")


# Delete a calendar by its ID
def delete_calendar(calendar_id):
    # Delete the calendar
    query = "DELETE FROM calendars WHERE calendar_id = %s"
    data = (calendar_id,)

    try:
        execute_query(query, data)
        logger.info(f"Deleted calendar with ID {calendar_id}")
        # Clean up orphaned meetings
        cleanup_orphaned_meetings()
    except Exception as e:
        logger.error(f"Error deleting calendar: {str(e)}")
        raise ValueError(f"Error deleting calendar: {str(e)}")


def cleanup_orphaned_meetings():
    # Find meetings that are not linked to any calendars
    query = """
    DELETE FROM meetings
    WHERE meeting_id NOT IN (SELECT DISTINCT meeting_id FROM scheduled_in)
    """
    try:
        execute_query(query)
        logger.info("Cleaned up orphaned meetings")
    except Exception as e:
        logger.error(f"Error cleaning up orphaned meetings: {str(e)}")
        raise ValueError(f"Error cleaning up orphaned meetings: {str(e)}")
