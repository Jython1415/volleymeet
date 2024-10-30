import logging
from flask import Blueprint, jsonify, request, abort
from queries import (
    create_attachment,
    update_attachment,
    get_all_attachments,
    get_attachment_by_id,
    delete_attachment,
    delete_attachments_by_meeting,
)

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Create a Blueprint for attachment routes
routes = Blueprint("attachment_routes", __name__, url_prefix='/')

# Endpoint to get all attachments
@routes.route("/attachments", methods=["GET"])
def api_get_attachments():
    logger.info("Fetching all attachments")
    try:
        attachments = get_all_attachments()
        logger.info("Successfully fetched attachments")
        return jsonify(attachments), 200
    except ValueError as e:
        logger.error(f"Error fetching attachments: {str(e)}")
        abort(404, description=str(e))


# Endpoint to get a specific attachment by ID
@routes.route("/<string:attachment_id>", methods=["GET"])
def api_get_attachment(attachment_id):
    logger.info(f"Fetching attachment with ID: {attachment_id}")
    try:
        attachment = get_attachment_by_id(attachment_id)
        return jsonify(attachment), 200
    except ValueError as e:
        logger.error(f"Error fetching attachment: {str(e)}")
        abort(404, description=str(e))


# Endpoint to add a new attachment
@routes.route("", methods=["POST"])
def api_add_attachment():
    data = request.get_json()
    meeting_id = data.get("meeting_id")
    attachment_url = data.get("attachment_url")
    attachment_id = data.get("attachment_id")

    logger.info(f"Adding new attachment for meeting ID: {meeting_id}")
    try:
        create_attachment(meeting_id, attachment_url, attachment_id)
        return jsonify({"message": "Attachment created successfully"}), 201
    except ValueError as e:
        logger.error(f"Error creating attachment: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to update an existing attachment
@routes.route("/<string:attachment_id>", methods=["PUT"])
def api_update_attachment(attachment_id):
    data = request.get_json()
    meeting_id = data.get("meeting_id")
    attachment_url = data.get("attachment_url")

    logger.info(f"Updating attachment with ID: {attachment_id}")
    try:
        update_attachment(attachment_id, meeting_id, attachment_url)
        return jsonify({"message": "Attachment updated successfully"}), 200
    except ValueError as e:
        logger.error(f"Error updating attachment: {str(e)}")
        return jsonify({"error": str(e)}), 400


# Endpoint to delete an attachment by ID
@routes.route("/<string:attachment_id>", methods=["DELETE"])
def api_delete_attachment(attachment_id):
    logger.info(f"Deleting attachment with ID: {attachment_id}")
    try:
        delete_attachment(attachment_id)
        return jsonify({"message": "Attachment deleted successfully"}), 204
    except ValueError as e:
        logger.error(f"Error deleting attachment: {str(e)}")
        abort(404, description=str(e))


# Endpoint to delete attachments by meeting ID
@routes.route(
    "/meetings/<string:meeting_id>", methods=["DELETE"]
)
def api_delete_attachments_by_meeting(meeting_id):
    logger.info(f"Deleting attachments for meeting with ID: {meeting_id}")
    try:
        delete_attachments_by_meeting(meeting_id)
        return jsonify({"message": "Attachments deleted successfully"}), 204
    except ValueError as e:
        logger.error(f"Error deleting attachments: {str(e)}")
        abort(404, description=str(e))
