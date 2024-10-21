import logging
import requests
from flask import Blueprint, jsonify, request, abort
from meetings_sql_queries import (
    create_meeting,
    get_all_meetings,
    get_meeting_by_id,
    update_meeting,
    delete_meeting,
)

ATTACHMENTS_BACKEND_BASE_URL = "http://localhost:5004/attachments"

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Create a Blueprint for meeting routes
meeting_routes = Blueprint("meeting_routes", __name__)


# Endpoint to get all meetings
@meeting_routes.route("/meetings", methods=["GET"])
def api_get_meetings():
    logger.info("Fetching all meetings")
    meetings = get_all_meetings()

    if "error" in meetings:
        logger.error("No meetings found")
        abort(404, description=meetings["error"])

    return jsonify(meetings), 200


# Endpoint to get a specific meeting by ID
@meeting_routes.route("/meetings/<string:meeting_id>", methods=["GET"])
def api_get_meeting(meeting_id):
    logger.info(f"Fetching meeting with ID: {meeting_id}")
    meeting = get_meeting_by_id(meeting_id)

    if "error" in meeting:
        logger.error(f"Meeting with ID {meeting_id} not found")
        abort(404, description=meeting["error"])

    return jsonify(meeting), 200


# Endpoint to add a new meeting
@meeting_routes.route("/meetings", methods=["POST"])
def api_add_meeting():
    data = request.get_json()

    title = data.get("title")
    date_time = data.get("date_time")
    location = data.get("location")
    details = data.get("details")

    # Meeting ID may not be specified
    meeting_id = data.get("meeting_id")

    logger.info(f"Adding new meeting with title: {title}")
    try:
        create_meeting(title, date_time, location, details, meeting_id)
        return jsonify({"message": "Meeting created successfully"}), 201
    except ValueError as e:
        logger.error(f"Error creating meeting: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to update an existing meeting
@meeting_routes.route("/meetings/<string:meeting_id>", methods=["PUT"])
def api_update_meeting(meeting_id):
    data = request.get_json()

    title = data.get("title")
    date_time = data.get("date_time")
    location = data.get("location")
    details = data.get("details")

    logger.info(f"Updating meeting with ID: {meeting_id}")
    try:
        update_meeting(meeting_id, title, date_time, location, details)
        return jsonify({"message": "Meeting updated successfully"}), 200
    except ValueError as e:
        logger.error(f"Error updating meeting with ID {meeting_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to delete a meeting by ID
@meeting_routes.route("/meetings/<string:meeting_id>", methods=["DELETE"])
def api_delete_meeting(meeting_id):
    logger.info(f"Deleting meeting with ID: {meeting_id}")
    try:
        delete_meeting(meeting_id)
        # delete attachments for that meeting (call the attachment service)
        # make a request to the attachment service to delete all attachments for this meeting
        requests.delete(
            f"{ATTACHMENTS_BACKEND_BASE_URL}/meetings/{meeting_id}"
        )  # TODO: make sure this is correct
        return jsonify({"message": "Meeting deleted successfully"}), 204
    except ValueError as e:
        logger.error(f"Meeting with ID {meeting_id} not found")
        abort(404, description=f"Meeting with ID {meeting_id} not found")


# Endpoint to link a meeting and participant
@meeting_routes.route(
    "/meetings/<string:meeting_id>/participants/<string:participant_id>",
    methods=["POST"],
)
def api_link_participant_to_meeting(meeting_id, participant_id):
    pass

# Endpoint to link a meeting and calendar
@meeting_routes.route(
    "/meetings/<string:meeting_id>/calendars/<string:calendar_id>",
    methods=["POST"],
)
def api_link_calendar_to_meeting(meeting_id, calendar_id):
    pass

# Endpoint to get all participants for a specific meeting
@meeting_routes.route("/meetings/<string:meeting_id>/participants", methods=["GET"])
def api_get_participants_for_meeting(meeting_id):
    pass
