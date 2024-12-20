import re
import uuid
import logging
from db_connection import execute_query, execute_read_query

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def is_valid_email(email):
    """Validates an email address using a regex."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


# Create a participant, including participant_id in the insert query
def create_participant(name, email, participant_id=None):
    if not is_valid_email(email):
        logger.error(f"Invalid email address: {email}")
        raise ValueError("Invalid email address")

    if participant_id is None:
        participant_id = str(uuid.uuid4())

    query = """
    INSERT INTO participants (participant_id, name, email)
    VALUES (%s, %s, %s)
    """
    data = (participant_id, name, email)
    try:
        execute_query(query, data)
        logger.info(f"Created participant with ID {participant_id}")
    except Exception as e:
        logger.error(f"Error creating participant: {str(e)}")
        raise ValueError(f"Error creating participant: {str(e)}")


# Update a participant by their ID
def update_participant(participant_id, name=None, email=None):
    # Fetch the current participant data using get_participant_by_id
    try:
        current_participant = get_participant_by_id(participant_id)
    except ValueError as e:
        raise ValueError(str(e))

    # Get the current values
    current_name = current_participant["name"]
    current_email = current_participant["email"]

    # Use the current value if the new value is None
    name = name if name is not None else current_name
    email = email if email is not None else current_email

    # Validate the new or existing email format
    if not is_valid_email(email):
        logger.error(f"Invalid email address: {email}")
        raise ValueError("Invalid email address")

    # Update the participant with the new or existing values
    update_query = """
    UPDATE participants 
    SET name = %s, email = %s
    WHERE participant_id = %s
    """
    update_data = (name, email, participant_id)

    try:
        execute_query(update_query, update_data)
        logger.info(f"Updated participant with ID {participant_id}")
    except Exception as e:
        logger.error(f"Error updating participant: {str(e)}")
        raise ValueError(f"Error updating participant: {str(e)}")


# Get all participants and return as formatted JSON
def get_all_participants():
    query = "SELECT * FROM participants"
    try:
        participants = execute_read_query(query)
    except Exception as e:
        logger.error(f"Error retrieving participants: {str(e)}")
        raise ValueError(f"Error retrieving participants: {str(e)}")

    if not participants:
        logger.info("No participants found")
        return []

    results = [
        {
            "participant_id": participant[0],
            "name": participant[1],
            "email": participant[2],
        }
        for participant in participants
    ]

    logger.info(f"Retrieved {len(results)} participants")
    return results


# Get a participant by their ID and return as formatted JSON
def get_participant_by_id(participant_id):
    query = "SELECT * FROM participants WHERE participant_id = %s"
    data = (participant_id,)
    
    try:
        participant = execute_read_query(query, data)
    except Exception as e:
        logger.error(f"Error retrieving participant: {str(e)}")
        raise ValueError(f"Error retrieving participant: {str(e)}")

    if not participant:
        logger.error(f"Participant with ID {participant_id} not found")
        return {"error": f"Participant with ID {participant_id} not found"}

    if len(participant) > 1:
        logger.error(f"Multiple participants found with ID {participant_id}")
        raise ValueError(f"Multiple participants found with ID {participant_id}")

    logger.info(f"Retrieved participant with ID {participant_id}")
    return {
        "participant_id": participant[0][0],
        "name": participant[0][1],
        "email": participant[0][2],
    }


# Delete a participant by their ID
def delete_participant(participant_id):
    # Delete the participant
    query = "DELETE FROM participants WHERE participant_id = %s"
    data = (participant_id,)

    try:
        execute_query(query, data)
        logger.info(f"Deleted participant with ID {participant_id}")
    except Exception as e:
        logger.error(f"Error deleting participant: {str(e)}")
        raise ValueError(f"Error deleting participant: {str(e)}")
