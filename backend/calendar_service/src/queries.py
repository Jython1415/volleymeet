import uuid
import logging
from db_connection import execute_query, execute_read_query

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


# Create a calendar, including calendar_id in the insert query
def create_calendar(title, details, calendar_id=None):
    # Generate a new UUID if calendar_id is not provided
    if not calendar_id:
        calendar_id = str(uuid.uuid4())

    query = """
    INSERT INTO calendars (calendar_id, title, details)
    VALUES (%s, %s, %s)
    """
    data = (calendar_id, title, details)

    try:
        execute_query(query, data)
        logger.info(f"Created calendar with ID {calendar_id}")
    except Exception as e:
        logger.error(f"Error creating calendar: {str(e)}")
        raise ValueError(f"Error creating calendar: {str(e)}")


# Update a calendar by its ID
def update_calendar(calendar_id, title=None, details=None):
    # Fetch the current calendar data using get_calendar_by_id function
    try:
        current_calendar = get_calendar_by_id(calendar_id)
    except ValueError as e:
        logger.error(f"Error finding calendar with ID {calendar_id}: {str(e)}")
        raise ValueError(f"Error finding calendar with ID {calendar_id}")

    # Use the current value if the new value is None
    title = title if title is not None else current_calendar["title"]
    details = details if details is not None else current_calendar["details"]

    # Update the calendar with the new or existing values
    update_query = """
    UPDATE calendars 
    SET title = %s, details = %s
    WHERE calendar_id = %s
    """
    update_data = (title, details, calendar_id)

    try:
        execute_query(update_query, update_data)
        logger.info(f"Updated calendar with ID {calendar_id}")
    except Exception as e:
        logger.error(f"Error updating calendar: {str(e)}")
        raise ValueError(f"Error updating calendar: {str(e)}")


# Get all calendars and return as formatted JSON
def get_all_calendars():
    query = "SELECT * FROM calendars"
    
    try:
        calendars = execute_read_query(query)
    except Exception as e:
        logger.error(f"Error retrieving calendars: {str(e)}")
        raise ValueError(f"Error retrieving calendars: {str(e)}")

    if not calendars:
        logger.info("No calendars found")
        return []

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

    try:
        calendar = execute_read_query(query, data)
    except Exception as e:
        logger.error(f"Error retrieving calendar with ID {calendar_id}: {str(e)}")
        raise ValueError(f"Error retrieving calendar with ID {calendar_id}: {str(e)}")

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
    except Exception as e:
        logger.error(f"Error deleting calendar: {str(e)}")
        raise ValueError(f"Error deleting calendar: {str(e)}")
