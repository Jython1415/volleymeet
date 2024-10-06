import json
from datetime import datetime
from managedb import execute_query, execute_read_query
from global_functions_sql import generate_uuid, is_valid_date


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
    data = (
        meeting_id,
        title,
        date_time,
        location,
        details,
    )

    execute_query(query, data)


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
    execute_query(query, data)


# Get all meetings and return as formatted JSON
def get_all_meetings():
    query = "SELECT * FROM meetings"
    meetings = execute_read_query(query)

    results = []
    for meeting in meetings:
        results.append(
            {
                "meeting_id": meeting[0],
                "title": meeting[1],
                "date_time": (
                    meeting[2].isoformat()
                    if isinstance(meeting[2], datetime)
                    else str(meeting[2])
                ),
                "location": meeting[3],
                "details": meeting[4],
            }
        )

    return json.dumps(results, default=str)


# Get a meeting by its ID and return as formatted JSON
def get_meeting_by_id(meeting_id):
    query = "SELECT * FROM meetings WHERE meeting_id = %s"
    data = (meeting_id,)
    meeting = execute_read_query(query, data)

    if meeting:
        return json.dumps(
            {
                "meeting_id": meeting[0][0],
                "title": meeting[0][1],
                "date_time": (
                    meeting[0][2].isoformat()
                    if isinstance(meeting[2], datetime)
                    else str(meeting[2])
                ),
                "location": meeting[0][3],
                "details": meeting[0][4],
            },
            default=str,
        )
    else:
        return json.dumps({"error": "Meeting not found"}, indent=4, default=str)


# Delete a meeting by its ID
def delete_meeting(meeting_id):
    query = "DELETE FROM meetings WHERE meeting_id = %s"
    data = (meeting_id,)
    execute_query(query, data)
