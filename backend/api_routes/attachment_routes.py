from flask import Blueprint, jsonify, request, abort
from models.attachments_sql_queries import (
    create_attachment,
    update_attachment,
    get_all_attachments,
    get_attachment_by_id,
    delete_attachment,
)

# Create a Blueprint for attachment routes
attachment_routes = Blueprint("attachment_routes", __name__)


# Endpoint to get all attachments
@attachment_routes.route("/attachments", methods=["GET"])
def api_get_attachments():
    """Fetch all attachments from the database."""
    attachments = get_all_attachments()

    if "error" in attachments:
        abort(404, description=attachments["error"])

    return jsonify(attachments), 200


# Endpoint to get a specific attachment by ID
@attachment_routes.route("/attachments/<string:attachment_id>", methods=["GET"])
def api_get_attachment(attachment_id):
    """Fetch a specific attachment by ID."""
    try:
        attachment = get_attachment_by_id(attachment_id)
        return jsonify(attachment), 200
    except ValueError as e:
        abort(404, description=str(e))


# Endpoint to add a new attachment
@attachment_routes.route("/attachments", methods=["POST"])
def api_add_attachment():
    """Add a new attachment to the database."""
    data = request.get_json()
    meeting_id = data.get("meeting_id")
    attachment_url = data.get("attachment_url")
    attachment_id = data.get("attachment_id")

    try:
        create_attachment(meeting_id, attachment_url, attachment_id)
        return jsonify({"message": "Attachment created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Endpoint to update an existing attachment
@attachment_routes.route("/attachments/<string:attachment_id>", methods=["PUT"])
def api_update_attachment(attachment_id):
    """Update an existing attachment by ID."""
    data = request.get_json()
    meeting_id = data.get("meeting_id")
    attachment_url = data.get("attachment_url")

    try:
        update_attachment(attachment_id, meeting_id, attachment_url)
        return jsonify({"message": "Attachment updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Endpoint to delete an attachment by ID
@attachment_routes.route("/attachments/<string:attachment_id>", methods=["DELETE"])
def api_delete_attachment(attachment_id):
    """Delete an attachment by ID."""
    try:
        delete_attachment(attachment_id)
        return jsonify({"message": "Attachment deleted successfully"}), 204
    except ValueError as e:
        abort(404, description=str(e))
