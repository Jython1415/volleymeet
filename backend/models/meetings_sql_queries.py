import json
from datetime import datetime
from scripts.managedb import execute_query, execute_read_query
from models.global_functions_sql import generate_uuid, is_valid_date


# Helper function to format dates in ISO format
def format_date(date_obj):
    if isinstance(date_obj, datetime):
        return date_obj.isoformat()
    return str(date_obj)


# Create a meeting, including meeting_id in the insert query
def create_meeting(title, date_time, location, details, meeting_id=None):
    # Generate a UUID for the meeting if not provided
    if not meeting_id:
        meeting_id = generate_uuid()

    # Validate the date format
    if not is_valid_date(date_time):
        raise ValueError("Date is not in a valid format")

    query = """
    INSERT INTO meetings (meeting_id, title, date_time, location, details)
    VALUES (%s, %s, %s, %s, %s)
    """
    data = (meeting_id, title, date_time, location, details)

    try:
        execute_query(query, data)
    except Exception as e:
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
    except Exception as e:
        raise ValueError(f"Error updating meeting: {str(e)}")


# Get all meetings and return as JSON
def get_all_meetings():
    query = "SELECT * FROM meetings"
    meetings = execute_read_query(query)

    if not meetings:
        return {"error": "No meetings found"}

    results = [
        {
            "meeting_id": meeting[0],
            "title": meeting[1],
            "date_time": format_date(meeting[2]),
            "location": meeting[3],
            "details": meeting[4],
        }
        for meeting in meetings
    ]

    return results


# Get a meeting by its ID and return as JSON
def get_meeting_by_id(meeting_id):
    query = "SELECT * FROM meetings WHERE meeting_id = %s"
    data = (meeting_id,)
    meeting = execute_read_query(query, data)

    if meeting:
        return {
            "meeting_id": meeting[0][0],
            "title": meeting[0][1],
            "date_time": format_date(meeting[0][2]),
            "location": meeting[0][3],
            "details": meeting[0][4],
        }
    else:
        return {"error": f"Meeting with ID {meeting_id} not found"}


# Delete a meeting by its ID
def delete_meeting(meeting_id):
    query = "DELETE FROM meetings WHERE meeting_id = %s"
    data = (meeting_id,)

    try:
        execute_query(query, data)
    except Exception as e:
        raise ValueError(f"Error deleting meeting: {str(e)}")
