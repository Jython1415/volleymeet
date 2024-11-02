import logging
import requests
from flask import Blueprint, jsonify, request, abort
from queries import (
    create_meeting,
    get_all_meetings,
    get_meeting_by_id,
    update_meeting,
    delete_meeting,
    get_participant_ids_for_meeting,
    get_participants_for_meeting,
)

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Create a Blueprint for meeting routes
routes = Blueprint("meeting_routes", __name__, url_prefix="/")


# Endpoint to get all meetings
@routes.route("", methods=["GET"])
def api_get_meetings():
    logger.info("Fetching all meetings")
    try:
        meetings = get_all_meetings()
        return jsonify(meetings), 200
    except ValueError as e:
        logger.error(f"Error fetching meetings: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to get a specific meeting by ID
@routes.route("/<string:meeting_id>", methods=["GET"])
def api_get_meeting(meeting_id):
    logger.info(f"Fetching meeting with ID: {meeting_id}")
    try:
        meeting = get_meeting_by_id(meeting_id)
        return jsonify(meeting), 200
    except ValueError as e:
        logger.error(f"Error fetching meeting with ID {meeting_id}: {str(e)}")
        return jsonify({"error": str(e)}), 404


# Endpoint to add a new meeting
@routes.route("", methods=["POST"])
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
@routes.route("/<string:meeting_id>", methods=["PUT"])
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
@routes.route("/<string:meeting_id>", methods=["DELETE"])
def api_delete_meeting(meeting_id):
    logger.info(f"Deleting meeting with ID: {meeting_id}")
    try:
        delete_meeting(meeting_id)
        
        # TODO: Delete attachments linked to this meeting
        # - call the attachment service
        # TODO: Delete participants orphaned by this deletion
        # - implement the orphan deletion logic in the linkage service
        # - expose an endpoint in the linkage service to delete orphaned participants
        # - call the linkage service
        # TODO: Delete calendars orphaned by this deletion
        # - implement the orphan deletion logic in the linkage service
        # - expose an endpoint in the linkage service to delete orphaned calendars
        # - call the linkage service
        
        return jsonify({"message": "Meeting deleted successfully"}), 204
    except ValueError as e:
        logger.error(f"Meeting with ID {meeting_id} not found")
        abort(404, description=f"Meeting with ID {meeting_id} not found")


# Endpoint to link a meeting and participant
@routes.route(
    "/<string:meeting_id>/participants/<string:participant_id>",
    methods=["POST"],
)
def api_link_participant_to_meeting(meeting_id, participant_id):
    # TODO: Reroute this request to the linkage service
    pass

# Endpoint to link a meeting and calendar
@routes.route(
    "/<string:meeting_id>/calendars/<string:calendar_id>",
    methods=["POST"],
)
def api_link_calendar_to_meeting(meeting_id, calendar_id):
    # TODO: Reroute this request to the linkage service
    pass

# Endpoint to get all participants for a specific meeting
@routes.route("/<string:meeting_id>/participants", methods=["GET"])
def api_get_participants_for_meeting(meeting_id):
    logger.info(f"Getting participants for meeting: {meeting_id}")
    try:
        participant_ids = requests.get(f"{LINKAGES_URL}/meetings/{meeting_id}/participants")

        results = [
            {
                requests.get(f"{PARTICIPANTS_URL}/participants/participant_ids/{participant_id}")
            }
            for participant_id in participant_ids
        ]
        
        return jsonify(results), 200
    except ValueError as e:
        logger.error(f"Error fetching participants for meeting: {str(e)}")

    # TODO: Find all participants linked to this meeting
    # - implement the logic in the linkage service
    # - expose an endpoint in the linkage service to get all participants linked to a meeting
    # - call the linkage service
    # TODO: Get the participants' details
    # - call the participant service
    # TODO: Return the participants' details in the expected format
    # - check the expected format by referencing the previous implementation
    # - return the participants' details in the expected format
