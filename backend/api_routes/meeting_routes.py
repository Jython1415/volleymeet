from flask import Blueprint, jsonify, request, abort
from models.meetings_sql_queries import (
    create_meeting,
    get_all_meetings,
    get_meeting_by_id,
    update_meeting,
    delete_meeting,
)

# Create a Blueprint for meeting routes
meeting_routes = Blueprint("meeting_routes", __name__)


# Endpoint to get all meetings
@meeting_routes.route("/meetings", methods=["GET"])
def api_get_meetings():
    """Fetch all meetings from the database."""
    meetings = get_all_meetings()

    if "error" in meetings:
        abort(404, description=meetings["error"])

    return jsonify(meetings), 200


# Endpoint to get a specific meeting by ID
@meeting_routes.route("/meetings/<string:meeting_id>", methods=["GET"])
def api_get_meeting(meeting_id):
    """Fetch a specific meeting by ID."""
    meeting = get_meeting_by_id(meeting_id)

    if "error" in meeting:
        abort(404, description=meeting["error"])

    return jsonify(meeting), 200


# Endpoint to add a new meeting
@meeting_routes.route("/meetings", methods=["POST"])
def api_add_meeting():
    """Add a new meeting to the database."""
    data = request.get_json()

    title = data.get("title")
    date_time = data.get("date_time")
    location = data.get("location")
    details = data.get("details")
    meeting_id = data.get("meeting_id")

    try:
        create_meeting(title, date_time, location, details, meeting_id)
        return jsonify({"message": "Meeting created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Endpoint to update an existing meeting
@meeting_routes.route("/meetings/<string:meeting_id>", methods=["PUT"])
def api_update_meeting(meeting_id):
    """Update an existing meeting by ID."""
    data = request.get_json()

    title = data.get("title")
    date_time = data.get("date_time")
    location = data.get("location")
    details = data.get("details")

    try:
        update_meeting(meeting_id, title, date_time, location, details)
        return jsonify({"message": "Meeting updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Endpoint to delete a meeting by ID
@meeting_routes.route("/meetings/<string:meeting_id>", methods=["DELETE"])
def api_delete_meeting(meeting_id):
    """Delete a meeting by ID."""
    try:
        delete_meeting(meeting_id)
        return jsonify({"message": "Meeting deleted successfully"}), 204
    except ValueError as e:
        abort(404, description=f"Meeting with ID {meeting_id} not found")
