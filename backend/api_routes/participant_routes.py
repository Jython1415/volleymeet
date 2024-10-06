from flask import Blueprint, jsonify, request, abort
from models.participants_sql_queries import (
    create_participant,
    update_participant,
    get_all_participants,
    get_participant_by_id,
    delete_participant,
)

# Create a Blueprint for participant routes
participant_routes = Blueprint("participant_routes", __name__)


# Endpoint to get all participants
@participant_routes.route("/participants", methods=["GET"])
def api_get_participants():
    """Fetch all participants from the database."""
    participants = get_all_participants()

    if "error" in participants:
        abort(404, description=participants["error"])

    return jsonify(participants), 200


# Endpoint to get a specific participant by ID
@participant_routes.route("/participants/<string:participant_id>", methods=["GET"])
def api_get_participant(participant_id):
    """Fetch a specific participant by ID."""
    participant = get_participant_by_id(participant_id)

    if "error" in participant:
        abort(404, description=participant["error"])

    return jsonify(participant), 200


# Endpoint to add a new participant
@participant_routes.route("/participants", methods=["POST"])
def api_add_participant():
    """Add a new participant to the database."""
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    participant_id = data.get("participant_id")

    try:
        create_participant(name, email, participant_id)
        return jsonify({"message": "Participant created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Endpoint to update an existing participant
@participant_routes.route("/participants/<string:participant_id>", methods=["PUT"])
def api_update_participant(participant_id):
    """Update an existing participant by ID."""
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    try:
        update_participant(participant_id, name, email)
        return jsonify({"message": "Participant updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Endpoint to delete a participant by ID
@participant_routes.route("/participants/<string:participant_id>", methods=["DELETE"])
def api_delete_participant(participant_id):
    """Delete a participant by ID."""
    try:
        delete_participant(participant_id)
        return jsonify({"message": "Participant deleted successfully"}), 204
    except ValueError as e:
        abort(404, description=f"Participant with ID {participant_id} not found")
