import logging
from flask import Blueprint, jsonify, request, abort
from queries import (
    create_participant,
    update_participant,
    get_all_participants,
    get_participant_by_id,
    delete_participant,
)

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Create a Blueprint for participant routes
routes = Blueprint("participant_routes", __name__, url_prefix="/")


# Endpoint to get all participants
@routes.route("", methods=["GET"])
def api_get_participants():
    logger.info("Fetching all participants")
    try:
        participants = get_all_participants()
        return jsonify(participants), 200
    except ValueError as e:
        logger.error(f"Error fetching participants: {str(e)}")
        abort(404, description=str(e))


# Endpoint to get a specific participant by ID
@routes.route("/<string:participant_id>", methods=["GET"])
def api_get_participant(participant_id):
    logger.info(f"Fetching participant with ID: {participant_id}")
    try:
        participant = get_participant_by_id(participant_id)
        return jsonify(participant), 200
    except ValueError as e:
        logger.error(f"Error fetching participant: {str(e)}")
        abort(404, description=str(e))


# Endpoint to add a new participant
@routes.route("", methods=["POST"])
def api_add_participant():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    participant_id = data.get("participant_id")

    logger.info(f"Adding new participant with name: {name}")
    try:
        create_participant(name, email, participant_id)
        return jsonify({"message": "Participant created successfully"}), 201
    except ValueError as e:
        logger.error(f"Error creating participant: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to update an existing participant
@routes.route("/<string:participant_id>", methods=["PUT"])
def api_update_participant(participant_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    logger.info(f"Updating participant with ID: {participant_id}")
    try:
        update_participant(participant_id, name, email)
        return jsonify({"message": "Participant updated successfully"}), 200
    except ValueError as e:
        logger.error(f"Error updating participant: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to delete a participant by ID
@routes.route("/<string:participant_id>", methods=["DELETE"])
def api_delete_participant(participant_id):
    logger.info(f"Deleting participant with ID: {participant_id}")
    try:
        delete_participant(participant_id)
        
        # TODO: Delete meetings that were orphaned by this deletion
        # - Implement the logic for this in the linkage service
        #   - The linkage service will have to call the meeting service to do this
        # - Call the linkage service to delete orphaned meetings
        
        return jsonify({"message": "Participant deleted successfully"}), 204
    except ValueError as e:
        logger.error(f"Participant with ID {participant_id} not found")
        abort(404, description=f"Participant with ID {participant_id} not found")
