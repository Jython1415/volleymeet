import logging
from datetime import datetime
from scripts.managedb import execute_query, execute_read_query

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


# Helper function to format dates in ISO format
def format_date(date_obj):
    if isinstance(date_obj, datetime):
        return date_obj.isoformat()
    return str(date_obj)


def link_participant_to_meeting(meeting_id, participant_id):
    # Insert a new record into the participating_in table
    query = """
    INSERT INTO participating_in (meeting_id, participant_id)
    VALUES (%s, %s)
    """
    data = (meeting_id, participant_id)

    try:
        execute_query(query, data)
        logger.info(f"Linked participant {participant_id} to meeting {meeting_id}")
    except Exception as e:
        logger.error(
            f"Error linking participant {participant_id} to meeting {meeting_id}: {str(e)}"
        )
        raise ValueError(
            f"Error linking participant {participant_id} to meeting {meeting_id}: {str(e)}"
        )


def link_calendar_to_meeting(meeting_id, calendar_id):
    # Insert a new record into the scheduled_in table
    query = """
    INSERT INTO scheduled_in (meeting_id, calendar_id)
    VALUES (%s, %s)
    """
    data = (meeting_id, calendar_id)

    try:
        execute_query(query, data)
        logger.info(f"Linked calendar {calendar_id} to meeting {meeting_id}")
    except Exception as e:
        logger.error(
            f"Error linking calendar {calendar_id} to meeting {meeting_id}: {str(e)}"
        )
        raise ValueError(
            f"Error linking calendar {calendar_id} to meeting {meeting_id}: {str(e)}"
        )
    
def get_participants_from_meeting_id(meeting_id):
    query = """GET * FROM participating_in WHERE meeting_id = %s"""
    data = (meeting_id,)

    try:
        participant_ids = execute_query(query, data)
        logger.info(f"Retrieved participants with meeting {meeting_id}")
    except Exception as e:
        logger.error(
            f"Error retrieving participants from meeting {meeting_id}: {str(e)}"
        )

    return participant_ids
    

