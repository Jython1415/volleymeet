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
def update_meeting(meeting_id, title, date_time, location, details):
    # Validate the date format
    if not is_valid_date(date_time):
        raise ValueError("Date is not in a valid format")

    query = """
    UPDATE meetings 
    SET title = %s, date_time = %s, location = %s, details = %s
    WHERE meeting_id = %s
    """
    data = (title, date_time, location, details, meeting_id)

    try:
        execute_query(query, data)
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
