import json
from scripts.managedb import execute_query, execute_read_query
from models.global_functions_sql import generate_uuid


# Create a calendar, including meeting_ids in the insert query
def create_calendar(title, details, calendar_id=None):
    # Generate a UUID for the calendar if not provided
    if not calendar_id:
        calendar_id = generate_uuid()

    query = """
    INSERT INTO calendars (calendar_id, title, details)
    VALUES (%s, %s, %s)
    """
    data = (calendar_id, title, details)
    execute_query(query, data)


# Update a calendar by its ID
def update_calendar(calendar_id, title, details):
    query = """
    UPDATE calendars 
    SET title = %s, details = %s
    WHERE calendar_id = %s
    """
    data = (title, details, calendar_id)
    execute_query(query, data)


# Get all calendars and return as formatted JSON
def get_all_calendars():
    query = "SELECT * FROM calendars"
    calendars = execute_read_query(query)

    results = []
    for calendar in calendars:
        results.append(
            {
                "calendar_id": calendar[0],
                "title": calendar[1],
                "details": calendar[2],
            }
        )

    return json.dumps(results, indent=4)


# Get a calendar by its ID and return as formatted JSON
def get_calendar_by_id(calendar_id):
    query = "SELECT * FROM calendars WHERE calendar_id = %s"
    data = (calendar_id,)
    calendar = execute_read_query(query, data)

    if calendar:
        return json.dumps(
            {
                "calendar_id": calendar[0][0],
                "title": calendar[0][1],
                "details": calendar[0][2],
            },
            indent=4,
        )
    else:
        return json.dumps({"error": "Calendar not found"}, indent=4)


# Delete a calendar by its ID
def delete_calendar(calendar_id):
    query = "DELETE FROM calendars WHERE calendar_id = %s"
    data = (calendar_id,)
    execute_query(query, data)
