import logging
from flask import Blueprint, jsonify, request, abort
from models.attachments_sql_queries import (
    create_attachment,
    update_attachment,
    get_all_attachments,
    get_attachment_by_id,
    delete_attachment,
)

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Create a Blueprint for attachment routes
attachment_routes = Blueprint("attachment_routes", __name__)


# Endpoint to get all attachments
@attachment_routes.route("/attachments", methods=["GET"])
def api_get_attachments():
    """Fetch all attachments from the database."""
    logger.info("Fetching all attachments")
    attachments = get_all_attachments()

    if "error" in attachments:
        logger.error("No attachments found")
        abort(404, description=attachments["error"])

    logger.info("Successfully fetched attachments")
    return jsonify(attachments), 200


# Endpoint to get a specific attachment by ID
@attachment_routes.route("/attachments/<string:attachment_id>", methods=["GET"])
def api_get_attachment(attachment_id):
    """Fetch a specific attachment by ID."""
    logger.info(f"Fetching attachment with ID: {attachment_id}")
    try:
        attachment = get_attachment_by_id(attachment_id)
        logger.info(f"Successfully fetched attachment with ID: {attachment_id}")
        return jsonify(attachment), 200
    except ValueError as e:
        logger.error(f"Error fetching attachment with ID {attachment_id}: {str(e)}")
        abort(404, description=str(e))


# Endpoint to add a new attachment
@attachment_routes.route("/attachments", methods=["POST"])
def api_add_attachment():
    """Add a new attachment to the database."""
    data = request.get_json()
    meeting_id = data.get("meeting_id")
    attachment_url = data.get("attachment_url")
    attachment_id = data.get("attachment_id")

    logger.info(f"Adding new attachment for meeting ID: {meeting_id}")
    try:
        create_attachment(meeting_id, attachment_url, attachment_id)
        logger.info("Attachment created successfully")
        return jsonify({"message": "Attachment created successfully"}), 201
    except ValueError as e:
        logger.error(f"Error creating attachment: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to update an existing attachment
@attachment_routes.route("/attachments/<string:attachment_id>", methods=["PUT"])
def api_update_attachment(attachment_id):
    """Update an existing attachment by ID."""
    data = request.get_json()
    meeting_id = data.get("meeting_id")
    attachment_url = data.get("attachment_url")

    logger.info(f"Updating attachment with ID: {attachment_id}")
    try:
        update_attachment(attachment_id, meeting_id, attachment_url)
        logger.info(f"Attachment with ID {attachment_id} updated successfully")
        return jsonify({"message": "Attachment updated successfully"}), 200
    except ValueError as e:
        logger.error(f"Error updating attachment with ID {attachment_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to delete an attachment by ID
@attachment_routes.route("/attachments/<string:attachment_id>", methods=["DELETE"])
def api_delete_attachment(attachment_id):
    """Delete an attachment by ID."""
    logger.info(f"Deleting attachment with ID: {attachment_id}")
    try:
        delete_attachment(attachment_id)
        logger.info(f"Attachment with ID {attachment_id} deleted successfully")
        return jsonify({"message": "Attachment deleted successfully"}), 204
    except ValueError as e:
        logger.error(f"Error deleting attachment with ID {attachment_id}: {str(e)}")
        abort(404, description=str(e))
