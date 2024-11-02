import json
import requests
<<<<<<< HEAD
import random
import uuid
import logging
import pika
import time
from datetime import datetime, timedelta
BASE_URL = "http://localhost:5001"  # Modify the base URL if backend is hosted elsewhere
=======

ATTACHMENT_BASE_URL = "http://localhost:5001"
CALENDAR_BASE_URL = "http://localhost:5002"
MEETING_BASE_URL = "http://localhost:5004"
PARTICIPANT_BASE_URL = "http://localhost:5005"
>>>>>>> main

logging.basicConfig(level=logging.INFO)


# Function to connect to RabbitMQ
def connect_to_rabbitmq():
    connected = False
    connection = None
    channel = None

    while not connected:
        try:
            credentials = pika.PlainCredentials("rabbituser", "rabbitpassword")
            parameters = pika.ConnectionParameters("message_broker", 5672, "demo-vhost", credentials)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            logging.info("Connected to RabbitMQ")
            connected = True
        except pika.exceptions.AMQPConnectionError:
            logging.warning("Connection attempt failed, retrying in 5 seconds...")
            time.sleep(5)
    
    return connection, channel
    
# Helper function to create random string
def random_string(length):
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=length))

# Helper function to create invalid email
def random_invalid_email():
    return random_string(8)  # No "@" character

# Function to generate batch of meetings, participants, and attachments
# Function to generate and publish batch messages
def create_and_send_batch(batch_size=500, invalid_percentage=20):
    num_invalid_meetings = int((invalid_percentage / 100) * batch_size)

    # Connect to RabbitMQ
    connection, channel = connect_to_rabbitmq()

    invalid_counts = {
        "invalid_meeting_title": 0,
        "invalid_meeting_location": 0,
        "invalid_participant_name": 0,
        "invalid_participant_email": 0,
        "invalid_attachment_url": 0,
    }

    for i in range(batch_size):
        is_meeting_invalid = i < num_invalid_meetings  # Ensure 20% invalid entries

        # Create a meeting with potential invalid fields
        title = random_string(random.randint(20, 2500)) if is_meeting_invalid else random_string(random.randint(20, 200))
        if len(title) > 2000:
            invalid_counts["invalid_meeting_title"] += 1

        location = random_string(random.randint(10, 2500)) if is_meeting_invalid else random_string(random.randint(10, 200))
        if len(location) > 2000:
            invalid_counts["invalid_meeting_location"] += 1

        meeting = {
            "meeting_id": str(uuid.uuid4()),
            "title": title,
            "date_time": (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %I:%M %p"),
            "location": location,
            "details": random_string(random.randint(20, 5000))
        }

        participants = []
        for j in range(random.randint(50, 100)):
            is_participant_invalid = j < int(invalid_percentage / 100 * 50)
            
            name = random_string(random.randint(5, 650)) if is_participant_invalid else random_string(random.randint(5, 50))
            if len(name) > 600:
                invalid_counts["invalid_participant_name"] += 1

            email = random_invalid_email() if is_participant_invalid else f"{random_string(5)}@example.com"
            if "@" not in email:
                invalid_counts["invalid_participant_email"] += 1

            participant = {
                "participant_id": str(uuid.uuid4()),
                "meeting_id": meeting["meeting_id"],
                "name": name,
                "email": email
            }
            participants.append(participant)

        attachments = []
        for k in range(random.randint(5, 10)):
            is_attachment_invalid = k < int(invalid_percentage / 100 * 10)

            url_prefix = "" if is_attachment_invalid else "http://example.com/"
            url = f"{url_prefix}{random_string(10)}.pdf"
            if not url.startswith("http"):
                invalid_counts["invalid_attachment_url"] += 1

            attachment = {
                "attachment_id": str(uuid.uuid4()),
                "meeting_id": meeting["meeting_id"],
                "url": url
            }
            attachments.append(attachment)

        meeting_message = {
            "meeting_id": meeting["meeting_id"],
            "title": meeting["title"],
            "date_time": meeting["date_time"],
            "location": meeting["location"],
            "details": meeting["details"],
            "participants": participants,
            "attachments": attachments
        }

        # Publish message to the "meetings" queue
        message = json.dumps(meeting_message)
        channel.basic_publish(
            exchange='',
            routing_key='meetings',
            body=message
        )
        logging.info(f"Sent message: {meeting_message['meeting_id']}")

    # Log invalid counts
    logging.info("Batch Processing Complete")
    logging.info("Invalid Data Summary:")
    for key, count in invalid_counts.items():
        logging.info(f"{key}: {count}")

    # Close connection to RabbitMQ
    connection.close()

# New function to send batch data as HTTP requests
def send_batch_data(batch_data):
    success_counts = {
        "meetings": 0,
        "participants": 0,
        "attachments": 0
    }
    failure_counts = {
        "meetings": 0,
        "participants": 0,
        "attachments": 0
    }

    # Process each meeting in the batch data
    for meeting in batch_data["meetings"]:
        # Send meeting
        meeting_response = requests.post(f"{BASE_URL}/meetings", json=meeting)
        if meeting_response.status_code == 201:
            success_counts["meetings"] += 1
        else:
            failure_counts["meetings"] += 1

        # Send participants for the meeting
        for participant in meeting["participants"]:
            participant_response = requests.post(f"{BASE_URL}/participants", json=participant)
            if participant_response.status_code == 201:
                success_counts["participants"] += 1
            else:
                failure_counts["participants"] += 1

        # Send attachments for the meeting
        for attachment in meeting["attachments"]:
            attachment_response = requests.post(f"{BASE_URL}/attachments", json=attachment)
            if attachment_response.status_code == 201:
                success_counts["attachments"] += 1
            else:
                failure_counts["attachments"] += 1

    # Log summary of successful and failed requests at the end
    logging.info("Batch Sending Complete")
    logging.info("Summary of Batch Results:")
    logging.info(f"Meetings - Success: {success_counts['meetings']}, Failures: {failure_counts['meetings']}")
    logging.info(f"Participants - Success: {success_counts['participants']}, Failures: {failure_counts['participants']}")
    logging.info(f"Attachments - Success: {success_counts['attachments']}, Failures: {failure_counts['attachments']}")

    return "Batch data sent successfully."



# Attachment Services
def get_all_attachments():
    response = requests.get(f"{ATTACHMENT_BASE_URL}")
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        attachments = response.json()
        for attachment in attachments:
            print(attachment)  # Print each attachment on a new line
    else:
        return f"Error fetching attachments: {response.text}"

def get_attachment_by_id(attachment_id):
    response = requests.get(f"{ATTACHMENT_BASE_URL}/{attachment_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error fetching attachment {attachment_id}: {response.text}"

def create_attachment(meeting_id, attachment_url, attachment_id=None):
    data = {"meeting_id": meeting_id, "attachment_url": attachment_url, "attachment_id": attachment_id}
    response = requests.post(f"{ATTACHMENT_BASE_URL}", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error creating attachment: {response.text}"

def update_attachment(attachment_id, meeting_id, attachment_url):
    data = {"meeting_id": meeting_id, "attachment_url": attachment_url}
    response = requests.put(f"{ATTACHMENT_BASE_URL}/{attachment_id}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error updating attachment {attachment_id}: {response.text}"

def delete_attachment(attachment_id):
    response = requests.delete(f"{ATTACHMENT_BASE_URL}/{attachment_id}")
    if response.status_code == 204:
        return "Attachment deleted successfully"
    else:
        return f"Error deleting attachment {attachment_id}: {response.text}"


# Calendar Services
def get_all_calendars():
    response = requests.get(f"{CALENDAR_BASE_URL}")
    if response.status_code == 200:
        calendars = response.json()
        for calendar in calendars:
            print(calendar)  # Print each calendar on a new line
    else:
        return f"Error fetching calendars: {response.text}"

def get_calendar_by_id(calendar_id):
    response = requests.get(f"{CALENDAR_BASE_URL}/{calendar_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error fetching calendar {calendar_id}: {response.text}"

def create_calendar(title, details, calendar_id=None):
    data = {"title": title, "details": details, "calendar_id": calendar_id}
    response = requests.post(f"{CALENDAR_BASE_URL}", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error creating calendar: {response.text}"

def update_calendar(calendar_id, title, details):
    data = {"title": title, "details": details}
    response = requests.put(f"{CALENDAR_BASE_URL}/{calendar_id}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error updating calendar {calendar_id}: {response.text}"

def delete_calendar(calendar_id):
    response = requests.delete(f"{CALENDAR_BASE_URL}/{calendar_id}")
    if response.status_code == 204:
        return "Calendar deleted successfully"
    else:
        return f"Error deleting calendar {calendar_id}: {response.text}"

def get_meetings_for_calendar(calendar_id):
    response = requests.get(f"{CALENDAR_BASE_URL}/{calendar_id}/meetings")
    if response.status_code == 200:
        meetings = response.json()
        for meeting in meetings:
            print(meeting)  # Print each meeting on a new line
    else:
        return f"Error fetching meetings for calendar {calendar_id}: {response.text}"


# Meeting Services
def get_all_meetings():
    response = requests.get(f"{MEETING_BASE_URL}")
    if response.status_code == 200:
        meetings = response.json()
        for meeting in meetings:
            print(meeting)  # Print each meeting on a new line
    else:
        return f"Error fetching meetings: {response.text}"

def get_meeting_by_id(meeting_id):
    response = requests.get(f"{MEETING_BASE_URL}/{meeting_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error fetching meeting {meeting_id}: {response.text}"

def create_meeting(title, date_time, location, details, meeting_id=None):
    data = {"title": title, "date_time": date_time, "location": location, "details": details, "meeting_id": meeting_id}
    response = requests.post(f"{MEETING_BASE_URL}", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error creating meeting: {response.text}"

def update_meeting(meeting_id, title, date_time, location, details):
    data = {"title": title, "date_time": date_time, "location": location, "details": details}
    response = requests.put(f"{MEETING_BASE_URL}/{meeting_id}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error updating meeting {meeting_id}: {response.text}"

def delete_meeting(meeting_id):
    response = requests.delete(f"{MEETING_BASE_URL}/{meeting_id}")
    if response.status_code == 204:
        return "Meeting deleted successfully"
    else:
        return f"Error deleting meeting {meeting_id}: {response.text}"

def link_participant_to_meeting(meeting_id, participant_id):
    response = requests.post(f"{MEETING_BASE_URL}/{meeting_id}/participants/{participant_id}")
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error linking participant {participant_id} to meeting {meeting_id}: {response.text}"

def link_calendar_to_meeting(meeting_id, calendar_id):
    response = requests.post(f"{MEETING_BASE_URL}/{meeting_id}/calendars/{calendar_id}")
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error linking calendar {calendar_id} to meeting {meeting_id}: {response.text}"

def get_participants_for_meeting(meeting_id):
    response = requests.get(f"{MEETING_BASE_URL}/{meeting_id}/participants")
    if response.status_code == 200:
        participants = response.json()
        for participant in participants:
            print(participant)  # Print each participant on a new line
    else:
        return f"Error fetching participants for meeting {meeting_id}: {response.text}"


# Participant Services
def get_all_participants():
    response = requests.get(f"{PARTICIPANT_BASE_URL}")
    if response.status_code == 200:
        participants = response.json()
        for participant in participants:
            print(participant)  # Print each participant on a new line
    else:
        return f"Error fetching participants: {response.text}"

def get_participant_by_id(participant_id):
    response = requests.get(f"{PARTICIPANT_BASE_URL}/{participant_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error fetching participant {participant_id}: {response.text}"

def create_participant(name, email, participant_id=None):
    data = {"name": name, "email": email, "participant_id": participant_id}
    response = requests.post(f"{PARTICIPANT_BASE_URL}", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error creating participant: {response.text}"

def update_participant(participant_id, name, email):
    data = {"name": name, "email": email}
    response = requests.put(f"{PARTICIPANT_BASE_URL}/{participant_id}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error updating participant {participant_id}: {response.text}"

def delete_participant(participant_id):
    response = requests.delete(f"{PARTICIPANT_BASE_URL}/{participant_id}")
    if response.status_code == 204:
        return "Participant deleted successfully"
    else:
        return f"Error deleting participant {participant_id}: {response.text}"
