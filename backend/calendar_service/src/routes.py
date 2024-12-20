import logging
from flask import Blueprint, jsonify, request, abort
from queries import (
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
routes = Blueprint("calendar_routes", __name__, url_prefix="/")


# Endpoint to get all calendars
@routes.route("", methods=["GET"])
def api_get_calendars():
    logger.info("Fetching all calendars")
    try:
        calendars = get_all_calendars()
        return jsonify(calendars), 200
    except ValueError as e:
        logger.error(f"Error fetching calendars: {str(e)}")
        abort(404, description=str(e))


# Endpoint to get a specific calendar by ID
@routes.route("/<string:calendar_id>", methods=["GET"])
def api_get_calendar(calendar_id):
    logger.info(f"Fetching calendar with ID: {calendar_id}")
    try:
        calendar = get_calendar_by_id(calendar_id)
        return jsonify(calendar), 200
    except ValueError as e:
        logger.error(f"Error fetching calendar: {str(e)}")
        abort(404, description=str(e))


# Endpoint to add a new calendar
@routes.route("", methods=["POST"])
def api_add_calendar():
    data = request.get_json()
    title = data.get("title")
    details = data.get("details")
    calendar_id = data.get("calendar_id")

    logger.info(f"Adding new calendar with title: {title}")
    try:
        create_calendar(title, details, calendar_id)
        return jsonify({"message": "Calendar created successfully"}), 201
    except ValueError as e:
        logger.error(f"Error creating calendar: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to update an existing calendar
@routes.route("/<string:calendar_id>", methods=["PUT"])
def api_update_calendar(calendar_id):
    data = request.get_json()
    title = data.get("title")
    details = data.get("details")

    logger.info(f"Updating calendar with ID: {calendar_id}")
    try:
        update_calendar(calendar_id, title, details)
        return jsonify({"message": "Calendar updated successfully"}), 200
    except ValueError as e:
        logger.error(f"Error updating calendar: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to delete a calendar by ID
@routes.route("/<string:calendar_id>", methods=["DELETE"])
def api_delete_calendar(calendar_id):
    logger.info(f"Deleting calendar with ID: {calendar_id}")
    try:
        delete_calendar(calendar_id)
        # TODO: find meetings that were orphaned by this deletion
        # - implement this in the linkage service
        # - call that route here
        # TODO: delete the meetings that were orphaned
        # - call the meetings service to delete them
        return jsonify({"message": "Calendar deleted successfully"}), 204
    except ValueError as e:
        logger.error(f"Error deleting calendar: {str(e)}")
        abort(404, description=str(e))


# Endpoint to get all meetings for a specific calendar
@routes.route("/<string:calendar_id>/meetings", methods=["GET"])
def api_get_meetings_for_calendar(calendar_id):
    # TODO: find meetings for a calendar
    # - implement this in the linkage service
    # - call that route here
    # TODO: find the details of the meetings
    # - call the meetings service to get the details
    # TODO: return the details of the meetings in the format required
    # - check the previous implementation for the format
    pass
