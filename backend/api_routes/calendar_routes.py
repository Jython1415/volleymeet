from flask import Blueprint, jsonify, request, abort
from models.calendars_sql_queries import (
    create_calendar,
    update_calendar,
    get_all_calendars,
    get_calendar_by_id,
    delete_calendar,
)

# Create a Blueprint for calendar routes
calendar_routes = Blueprint("calendar_routes", __name__)


# Endpoint to get all calendars
@calendar_routes.route("/calendars", methods=["GET"])
def api_get_calendars():
    """Fetch all calendars from the database."""
    calendars = get_all_calendars()

    if "error" in calendars:
        abort(404, description=calendars["error"])

    return jsonify(calendars), 200


# Endpoint to get a specific calendar by ID
@calendar_routes.route("/calendars/<string:calendar_id>", methods=["GET"])
def api_get_calendar(calendar_id):
    """Fetch a specific calendar by ID."""
    try:
        calendar = get_calendar_by_id(calendar_id)
        return jsonify(calendar), 200
    except ValueError as e:
        abort(404, description=str(e))


# Endpoint to add a new calendar
@calendar_routes.route("/calendars", methods=["POST"])
def api_add_calendar():
    """Add a new calendar to the database."""
    data = request.get_json()
    title = data.get("title")
    details = data.get("details")
    calendar_id = data.get("calendar_id")

    try:
        create_calendar(title, details, calendar_id)
        return jsonify({"message": "Calendar created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Endpoint to update an existing calendar
@calendar_routes.route("/calendars/<string:calendar_id>", methods=["PUT"])
def api_update_calendar(calendar_id):
    """Update an existing calendar by ID."""
    data = request.get_json()
    title = data.get("title")
    details = data.get("details")

    try:
        update_calendar(calendar_id, title, details)
        return jsonify({"message": "Calendar updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Endpoint to delete a calendar by ID
@calendar_routes.route("/calendars/<string:calendar_id>", methods=["DELETE"])
def api_delete_calendar(calendar_id):
    """Delete a calendar by ID."""
    try:
        delete_calendar(calendar_id)
        return jsonify({"message": "Calendar deleted successfully"}), 204
    except ValueError as e:
        abort(404, description=str(e))
