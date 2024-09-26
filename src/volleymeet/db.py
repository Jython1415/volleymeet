import sqlite3
from pathlib import Path
import uuid
import re

# Path to the SQLite database file
DB_PATH = Path("data/volleyball_meetings.db")


def get_connection():
    """Establishes a connection to the SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row  # Allows access by column names
    return connection


def generate_uuid():
    """Generates a UUID."""
    return str(uuid.uuid4())


def is_valid_email(email):
    """Validates an email address using a regex."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def initialize_database():
    """Initializes the database schema if it's not already created."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Create meetings table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS meetings (
                meeting_id TEXT PRIMARY KEY,
                title TEXT NOT NULL CHECK (LENGTH(title) <= 2000),
                details TEXT CHECK (LENGTH(details) <= 10000),
                location TEXT CHECK (LENGTH(location) <= 2000),
                date_time TEXT NOT NULL
            )
        """
        )

        # Create participants table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS participants (
                participant_id TEXT PRIMARY KEY,
                name TEXT NOT NULL CHECK (LENGTH(name) <= 600),
                email TEXT NOT NULL
            )
        """
        )

        # Create calendars table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS calendars (
                calendar_id TEXT PRIMARY KEY,
                title TEXT NOT NULL CHECK (LENGTH(title) <= 2000),
                details TEXT CHECK (LENGTH(details) <= 10000)
            )
        """
        )

        # Create attachments table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS attachments (
                attachment_id TEXT PRIMARY KEY,
                meeting_id TEXT NOT NULL,
                url TEXT NOT NULL,
                FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE
            )
        """
        )

        # Create participating_in table (many-to-many relationship)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS participating_in (
                participant_id TEXT NOT NULL,
                meeting_id TEXT NOT NULL,
                FOREIGN KEY (participant_id) REFERENCES participants(participant_id) ON DELETE CASCADE,
                FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE
            )
        """
        )

        # Create scheduled_in table (many-to-many relationship)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scheduled_in (
                meeting_id TEXT NOT NULL,
                calendar_id TEXT NOT NULL,
                FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE,
                FOREIGN KEY (calendar_id) REFERENCES calendars(calendar_id) ON DELETE CASCADE
            )
        """
        )

        conn.commit()


# --- Meetings ---


def add_meeting(title, details, location, date_time, meeting_id=None):
    """Adds a new meeting to the database."""
    if not meeting_id:
        meeting_id = generate_uuid()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO meetings (meeting_id, title, details, location, date_time)
            VALUES (?, ?, ?, ?, ?)
        """,
            (meeting_id, title, details, location, date_time),
        )
        conn.commit()


def update_meeting(meeting_id, title=None, details=None, location=None, date_time=None):
    """Updates an existing meeting."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Construct the dynamic SQL query based on the provided fields
        updates = []
        parameters = []

        if title:
            updates.append("title = ?")
            parameters.append(title)

        if details:
            updates.append("details = ?")
            parameters.append(details)

        if location:
            updates.append("location = ?")
            parameters.append(location)

        if date_time:
            updates.append("date_time = ?")
            parameters.append(date_time)

        if updates:
            # Only execute if there are fields to update
            query = f"UPDATE meetings SET {', '.join(updates)} WHERE meeting_id = ?"
            parameters.append(meeting_id)
            cursor.execute(query, parameters)
            conn.commit()


def delete_meeting(meeting_id):
    """Deletes a meeting and its associated records (attachments, participating_in, scheduled_in)."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Delete meeting (attachments, participating_in, and scheduled_in records will cascade)
        cursor.execute("DELETE FROM meetings WHERE meeting_id = ?", (meeting_id,))

        # Clean up orphaned participants
        cursor.execute(
            """
            DELETE FROM participants 
            WHERE participant_id NOT IN (SELECT DISTINCT participant_id FROM participating_in)
        """
        )

        # Clean up orphaned calendars (if no meetings are scheduled in them)
        cursor.execute(
            """
            DELETE FROM calendars 
            WHERE calendar_id NOT IN (SELECT DISTINCT calendar_id FROM scheduled_in)
        """
        )

        conn.commit()


# --- Participants ---


def add_participant(name, email, participant_id=None):
    """Adds a new participant to the database."""
    if not participant_id:
        participant_id = generate_uuid()

    if not is_valid_email(email):
        raise ValueError("Invalid email address")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO participants (participant_id, name, email)
            VALUES (?, ?, ?)
        """,
            (participant_id, name, email),
        )
        conn.commit()


def update_participant(participant_id, name=None, email=None):
    """Updates an existing participant."""
    with get_connection() as conn:
        cursor = conn.cursor()

        updates = []
        parameters = []

        if name:
            updates.append("name = ?")
            parameters.append(name)

        if email:
            if not is_valid_email(email):
                raise ValueError("Invalid email address")
            updates.append("email = ?")
            parameters.append(email)

        if updates:
            query = (
                f"UPDATE participants SET {', '.join(updates)} WHERE participant_id = ?"
            )
            parameters.append(participant_id)
            cursor.execute(query, parameters)
            conn.commit()


def delete_participant(participant_id):
    """Deletes a participant and their related records."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM participants WHERE participant_id = ?", (participant_id,)
        )

        # Clean up meetings where no participants are left
        cursor.execute(
            """
            DELETE FROM meetings
            WHERE meeting_id NOT IN (SELECT DISTINCT meeting_id FROM participating_in)
        """
        )
        conn.commit()


# --- Calendars ---


def add_calendar(title, details, calendar_id=None):
    """Adds a new calendar to the database."""
    if not calendar_id:
        calendar_id = generate_uuid()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO calendars (calendar_id, title, details)
            VALUES (?, ?, ?)
        """,
            (calendar_id, title, details),
        )
        conn.commit()


def update_calendar(calendar_id, title=None, details=None):
    """Updates an existing calendar."""
    with get_connection() as conn:
        cursor = conn.cursor()

        updates = []
        parameters = []

        if title:
            updates.append("title = ?")
            parameters.append(title)

        if details:
            updates.append("details = ?")
            parameters.append(details)

        if updates:
            query = f"UPDATE calendars SET {', '.join(updates)} WHERE calendar_id = ?"
            parameters.append(calendar_id)
            cursor.execute(query, parameters)
            conn.commit()


def delete_calendar(calendar_id):
    """Deletes a calendar and its related records."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM calendars WHERE calendar_id = ?", (calendar_id,))

        # Clean up meetings where no calendars are left
        cursor.execute(
            """
            DELETE FROM meetings
            WHERE meeting_id NOT IN (SELECT DISTINCT meeting_id FROM scheduled_in)
        """
        )
        conn.commit()


# --- Attachments ---


def add_attachment(meeting_id, url, attachment_id=None):
    """Adds a new attachment to a meeting."""
    if not attachment_id:
        attachment_id = generate_uuid()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO attachments (attachment_id, meeting_id, url)
            VALUES (?, ?, ?)
        """,
            (attachment_id, meeting_id, url),
        )
        conn.commit()


def update_attachment(attachment_id, url=None, meeting_id=None):
    """Updates an existing attachment."""
    with get_connection() as conn:
        cursor = conn.cursor()

        updates = []
        parameters = []

        if url:
            updates.append("url = ?")
            parameters.append(url)

        if meeting_id:
            updates.append("meeting_id = ?")
            parameters.append(meeting_id)

        if updates:
            query = (
                f"UPDATE attachments SET {', '.join(updates)} WHERE attachment_id = ?"
            )
            parameters.append(attachment_id)
            cursor.execute(query, parameters)
            conn.commit()


def delete_attachment(attachment_id):
    """Deletes an attachment from the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM attachments WHERE attachment_id = ?", (attachment_id,)
        )
        conn.commit()


# --- Additional Update Functions ---


def add_participant_to_meeting(meeting_id, participant_id):
    """Adds a participant to a meeting."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO participating_in (participant_id, meeting_id)
            VALUES (?, ?)
        """,
            (participant_id, meeting_id),
        )
        conn.commit()


def schedule_meeting_in_calendar(meeting_id, calendar_id):
    """Schedules a meeting in a calendar."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO scheduled_in (meeting_id, calendar_id)
            VALUES (?, ?)
        """,
            (meeting_id, calendar_id),
        )
        conn.commit()


# --- Additional List Functions ---


def list_calendars_for_meeting(meeting_id):
    """Lists all calendar IDs a meeting is scheduled in."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT calendar_id FROM scheduled_in WHERE meeting_id = ?
        """,
            (meeting_id,),
        )
        return [row["calendar_id"] for row in cursor.fetchall()]


def list_participants_for_meeting(meeting_id):
    """Lists all participant IDs for a meeting."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT participant_id FROM participating_in WHERE meeting_id = ?
        """,
            (meeting_id,),
        )
        return [row["participant_id"] for row in cursor.fetchall()]


def list_attachments_for_meeting(meeting_id):
    """Lists all attachment IDs for a meeting."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT attachment_id FROM attachments WHERE meeting_id = ?
        """,
            (meeting_id,),
        )
        return [row["attachment_id"] for row in cursor.fetchall()]


def list_meetings_in_calendar(calendar_id):
    """Lists all meeting IDs in a calendar."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT meeting_id FROM scheduled_in WHERE calendar_id = ?
        """,
            (calendar_id,),
        )
        return [row["meeting_id"] for row in cursor.fetchall()]


def list_meetings_for_participant(participant_id):
    """Lists all meeting IDs for a participant."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT meeting_id FROM participating_in WHERE participant_id = ?
        """,
            (participant_id,),
        )
        return [row["meeting_id"] for row in cursor.fetchall()]


def list_all_participants():
    """Lists all participants in the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM participants")
        return cursor.fetchall()


def list_all_calendars():
    """Lists all calendars in the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM calendars")
        return cursor.fetchall()


def list_all_meetings():
    """Lists all meetings in the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meetings")
        return cursor.fetchall()
