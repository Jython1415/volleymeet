import logging
from scripts.managedb import execute_query, execute_read_query
from models.global_functions_sql import is_valid_email

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


# Create a participant, including participant_id in the insert query
def create_participant(name, email, participant_id=None):
    if not is_valid_email(email):
        logger.error(f"Invalid email address: {email}")
        raise ValueError("Invalid email address")

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
    # Fetch the current participant data
    query = "SELECT name, email FROM participants WHERE participant_id = %s"
    data = (participant_id,)
    current_participant = execute_read_query(query, data)

    if not current_participant:
        logger.error(f"Participant with ID {participant_id} not found")
        raise ValueError(f"Participant with ID {participant_id} not found")

    # Get the current values
    current_name, current_email = current_participant[0]

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
    participants = execute_read_query(query)

    if not participants:
        logger.info("No participants found")
        return {"error": "No participants found"}

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
    participant = execute_read_query(query, data)

    if participant:
        logger.info(f"Retrieved participant with ID {participant_id}")
        return {
            "participant_id": participant[0][0],
            "name": participant[0][1],
            "email": participant[0][2],
        }
    else:
        logger.error(f"Participant with ID {participant_id} not found")
        return {"error": f"Participant with ID {participant_id} not found"}


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
