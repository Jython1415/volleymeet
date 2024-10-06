import logging
from flask import Blueprint, jsonify, request, abort
from models.calendars_sql_queries import (
    create_calendar,
    update_calendar,
    get_all_calendars,
    get_calendar_by_id,
    delete_calendar,
)

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Create a Blueprint for calendar routes
calendar_routes = Blueprint("calendar_routes", __name__)


# Endpoint to get all calendars
@calendar_routes.route("/calendars", methods=["GET"])
def api_get_calendars():
    """Fetch all calendars from the database."""
    logger.info("Fetching all calendars")
    calendars = get_all_calendars()

    if "error" in calendars:
        logger.error("No calendars found")
        abort(404, description=calendars["error"])

    logger.info("Successfully fetched calendars")
    return jsonify(calendars), 200


# Endpoint to get a specific calendar by ID
@calendar_routes.route("/calendars/<string:calendar_id>", methods=["GET"])
def api_get_calendar(calendar_id):
    """Fetch a specific calendar by ID."""
    logger.info(f"Fetching calendar with ID: {calendar_id}")
    try:
        calendar = get_calendar_by_id(calendar_id)
        logger.info(f"Successfully fetched calendar with ID: {calendar_id}")
        return jsonify(calendar), 200
    except ValueError as e:
        logger.error(f"Error fetching calendar with ID {calendar_id}: {str(e)}")
        abort(404, description=str(e))


# Endpoint to add a new calendar
@calendar_routes.route("/calendars", methods=["POST"])
def api_add_calendar():
    """Add a new calendar to the database."""
    data = request.get_json()
    title = data.get("title")
    details = data.get("details")
    calendar_id = data.get("calendar_id")

    logger.info(f"Adding new calendar with title: {title}")
    try:
        create_calendar(title, details, calendar_id)
        logger.info("Calendar created successfully")
        return jsonify({"message": "Calendar created successfully"}), 201
    except ValueError as e:
        logger.error(f"Error creating calendar: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to update an existing calendar
@calendar_routes.route("/calendars/<string:calendar_id>", methods=["PUT"])
def api_update_calendar(calendar_id):
    """Update an existing calendar by ID."""
    data = request.get_json()
    title = data.get("title")
    details = data.get("details")

    logger.info(f"Updating calendar with ID: {calendar_id}")
    try:
        update_calendar(calendar_id, title, details)
        logger.info(f"Calendar with ID {calendar_id} updated successfully")
        return jsonify({"message": "Calendar updated successfully"}), 200
    except ValueError as e:
        logger.error(f"Error updating calendar with ID {calendar_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to delete a calendar by ID
@calendar_routes.route("/calendars/<string:calendar_id>", methods=["DELETE"])
def api_delete_calendar(calendar_id):
    """Delete a calendar by ID."""
    logger.info(f"Deleting calendar with ID: {calendar_id}")
    try:
        delete_calendar(calendar_id)
        logger.info(f"Calendar with ID {calendar_id} deleted successfully")
        return jsonify({"message": "Calendar deleted successfully"}), 204
    except ValueError as e:
        logger.error(f"Error deleting calendar with ID {calendar_id}: {str(e)}")
        abort(404, description=str(e))
