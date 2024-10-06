import json
from scripts.managedb import execute_query, execute_read_query
from models.global_functions_sql import generate_uuid, is_valid_email


# Create a participant, including participant_id in the insert query
def create_participant(name, email, participant_id=None):
    if not participant_id:
        participant_id = generate_uuid()

    if not is_valid_email(email):
        raise ValueError("Invalid email address")

    query = """
    INSERT INTO participants (participant_id, name, email)
    VALUES (%s, %s, %s)
    """
    data = (participant_id, name, email)
    try:
        execute_query(query, data)
    except Exception as e:
        raise ValueError(f"Error creating participant: {str(e)}")


# Update a participant by their ID
def update_participant(participant_id, name, email):
    if not is_valid_email(email):
        raise ValueError("Invalid email address")

    query = """
    UPDATE participants 
    SET name = %s, email = %s
    WHERE participant_id = %s
    """
    data = (participant_id, name, email)
    try:
        execute_query(query, data)
    except Exception as e:
        raise ValueError(f"Error updating participant: {str(e)}")


# Get all participants and return as formatted JSON
def get_all_participants():
    query = "SELECT * FROM participants"
    participants = execute_read_query(query)

    if not participants:
        return {"error": "No participants found"}

    results = [
        {
            "participant_id": participant[0],
            "name": participant[1],
            "email": participant[2],
        }
        for participant in participants
    ]

    return results


# Get a participant by their ID and return as formatted JSON
def get_participant_by_id(participant_id):
    query = "SELECT * FROM participants WHERE participant_id = %s"
    data = (participant_id,)
    participant = execute_read_query(query, data)

    if participant:
        return (
            {
                "participant_id": participant[0][0],
                "name": participant[0][1],
                "email": participant[0][2],
            },
        )
    else:
        return {"error": f"Participant with ID {participant_id} not found"}


# Delete a participant by their ID
def delete_participant(participant_id):
    query = "DELETE FROM participants WHERE participant_id = %s"
    data = (participant_id,)

    try:
        execute_query(query, data)
    except Exception as e:
        raise ValueError(f"Error deleting participant: {str(e)}")
