import logging
from flask import Blueprint, jsonify, request, abort
from linkage_service.linkage_sql_queries import (
    link_participant_to_meeting,
    link_calendar_to_meeting,
    get_participants_from_meeting_id
)

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Create a Blueprint for meeting routes
meeting_routes = Blueprint("meeting_routes", __name__)

# Endpoint to link a meeting and participant
@meeting_routes.route(
    "/meetings/<string:meeting_id>/participants/<string:participant_id>",
    methods=["POST"],
)
def api_link_participant_to_meeting(meeting_id, participant_id):
    logger.info(f"Linking participant {participant_id} to meeting {meeting_id}")

    try:
        link_participant_to_meeting(meeting_id, participant_id)
        return (
            jsonify(
                {
                    "message": f"Participant {participant_id} linked to meeting {meeting_id} successfully"
                }
            ),
            201,
        )
    except ValueError as e:
        logger.error(
            f"Error linking participant {participant_id} to meeting {meeting_id}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 400


# Endpoint to link a meeting and calendar
@meeting_routes.route(
    "/meetings/<string:meeting_id>/calendars/<string:calendar_id>",
    methods=["POST"],
)
def api_link_calendar_to_meeting(meeting_id, calendar_id):
    logger.info(f"Linking calendar {calendar_id} to meeting {meeting_id}")

    try:
        link_calendar_to_meeting(meeting_id, calendar_id)
        return (
            jsonify(
                {
                    "message": f"Calendar {calendar_id} linked to meeting {meeting_id} successfully"
                }
            ),
            201,
        )
    except ValueError as e:
        logger.error(
            f"Error linking calendar {calendar_id} to meeting {meeting_id}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 400

# Endpoint to get participants from meeting
@meeting_routes.route(
    "/meetings/<string:meeting_id>/participants/<string:participant_id>",
    methods=["GET"],
)
def api_get_participants_from_meeting_id(meeting_id): 
    logger.info(f"Getting participants connected to meeting {meeting_id}")

    try:
        return get_participants_from_meeting_id(meeting_id)
    except ValueError as e:
        logger.error(
            f"Error getting participants from meeting {meeting_id}: {str(e)}"
        )
        return jsonify({"error": str(e)}), 400  # I have no idea if this is the right error
