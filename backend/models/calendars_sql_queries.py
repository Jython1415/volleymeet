import json
from scripts.managedb import execute_query, execute_read_query
from models.global_functions_sql import generate_uuid


# Create a calendar, including calendar_id in the insert query
def create_calendar(title, details, calendar_id=None):
    # Generate a UUID for the calendar if not provided
    if not calendar_id:
        calendar_id = generate_uuid()

    query = """
    INSERT INTO calendars (calendar_id, title, details)
    VALUES (%s, %s, %s)
    """
    data = (calendar_id, title, details)
    try:
        execute_query(query, data)
    except Exception as e:
        raise ValueError(f"Error creating calendar: {str(e)}")


# Update a calendar by its ID
def update_calendar(calendar_id, title=None, details=None):
    # Fetch the current calendar data
    query = "SELECT title, details FROM calendars WHERE calendar_id = %s"
    data = (calendar_id,)
    current_calendar = execute_read_query(query, data)

    if not current_calendar:
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
            raise ValueError(f"No calendar found with ID: {calendar_id}")
    except Exception as e:
        raise ValueError(f"Error updating calendar: {str(e)}")


# Get all calendars and return as formatted JSON
def get_all_calendars():
    query = "SELECT * FROM calendars"
    calendars = execute_read_query(query)

    if not calendars:
        return {"error": "No calendars found"}

    results = [
        {
            "calendar_id": calendar[0],
            "title": calendar[1],
            "details": calendar[2],
        }
        for calendar in calendars
    ]

    return results


# Get a calendar by its ID and return as formatted JSON
def get_calendar_by_id(calendar_id):
    query = "SELECT * FROM calendars WHERE calendar_id = %s"
    data = (calendar_id,)
    calendar = execute_read_query(query, data)

    if calendar:
        return {
            "calendar_id": calendar[0][0],
            "title": calendar[0][1],
            "details": calendar[0][2],
        }
    else:
        raise ValueError(f"Calendar with ID {calendar_id} not found")


# Delete a calendar by its ID
def delete_calendar(calendar_id):
    query = "DELETE FROM calendars WHERE calendar_id = %s"
    data = (calendar_id,)

    try:
        affected_rows = execute_query(query, data)
        if affected_rows == 0:
            raise ValueError(f"No calendar found with ID: {calendar_id}")
    except Exception as e:
        raise ValueError(f"Error deleting calendar: {str(e)}")
