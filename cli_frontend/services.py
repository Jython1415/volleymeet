import json
import random
import uuid
import logging
from datetime import datetime, timedelta
import requests

BASE_URL = "http://localhost:5001"  # Modify the base URL if backend is hosted elsewhere

logging.basicConfig(level=logging.INFO)

# Helper function to create random string
def random_string(length):
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=length))

# Helper function to create invalid email
def random_invalid_email():
    return random_string(8)  # No "@" character

# Function to generate batch of meetings, participants, and attachments
def create_batch(batch_size=500, invalid_percentage=20):
    batch_data = {"meetings": []}
    num_invalid_meetings = int((invalid_percentage / 100) * batch_size)

    # Counters for invalid data
    invalid_counts = {
        "invalid_meeting_title": 0,
        "invalid_meeting_location": 0,
        "invalid_participant_name": 0,
        "invalid_participant_email": 0,
        "invalid_attachment_url": 0,
    }

    for i in range(batch_size):
        is_invalid = i < num_invalid_meetings  # Control invalid entries

        # Create a new meeting with potential invalid fields
        title = random_string(random.randint(20, 2500)) if is_invalid else random_string(random.randint(20, 200))
        if len(title) > 2000:
            invalid_counts["invalid_meeting_title"] += 1

        location = random_string(random.randint(10, 2500)) if is_invalid else random_string(random.randint(10, 200))
        if len(location) > 2000:
            invalid_counts["invalid_meeting_location"] += 1

        meeting = {
            "meeting_id": str(uuid.uuid4()),
            "title": title,
            "date_time": (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %I:%M %p"),
            "location": location,
            "details": random_string(random.randint(20, 5000))
        }

        # Create participants
        participants = []
        for _ in range(random.randint(50, 100)):
            name = random_string(random.randint(5, 650)) if is_invalid and random.random() < 0.2 else random_string(random.randint(5, 50))
            if len(name) > 600:
                invalid_counts["invalid_participant_name"] += 1

            email = random_invalid_email() if is_invalid and random.random() < 0.2 else f"{random_string(5)}@example.com"
            if "@" not in email:
                invalid_counts["invalid_participant_email"] += 1
                
            participant = {
                "participant_id": str(uuid.uuid4()),
                "meeting_id": meeting["meeting_id"],
                "name": name,
                "email": email
            }
            participants.append(participant)

        # Create attachments
        attachments = []
        for _ in range(random.randint(5, 10)):
            url_prefix = "" if is_invalid and random.random() < 0.2 else "http://example.com/"
            url = f"{url_prefix}{random_string(10)}.pdf"
            if not url.startswith("http"):
                invalid_counts["invalid_attachment_url"] += 1

            attachment = {
                "attachment_id": str(uuid.uuid4()),
                "meeting_id": meeting["meeting_id"],
                "url": url
            }
            attachments.append(attachment)

        meeting["participants"] = participants
        meeting["attachments"] = attachments
        batch_data["meetings"].append(meeting)

    # Log the count of each invalid type at the end of processing
    logging.info("Batch Processing Complete")
    logging.info("Invalid Data Summary:")
    logging.info(f"Invalid Meetings (Title): {invalid_counts['invalid_meeting_title']}")
    logging.info(f"Invalid Meetings (Location): {invalid_counts['invalid_meeting_location']}")
    logging.info(f"Invalid Participants (Name): {invalid_counts['invalid_participant_name']}")
    logging.info(f"Invalid Participants (Email): {invalid_counts['invalid_participant_email']}")
    logging.info(f"Invalid Attachments (URL): {invalid_counts['invalid_attachment_url']}")

    # Log a sample of the data (first two meetings) for examination
    logging.info("Sample Batch Data (first 2 meetings):")
    logging.info(json.dumps(batch_data["meetings"][:2], indent=4))

    return batch_data

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
    response = requests.get(f"{BASE_URL}/attachments")
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        attachments = response.json()
        for attachment in attachments:
            print(attachment)  # Print each attachment on a new line
    else:
        return f"Error fetching attachments: {response.text}"

def get_attachment_by_id(attachment_id):
    response = requests.get(f"{BASE_URL}/attachments/{attachment_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error fetching attachment {attachment_id}: {response.text}"

def create_attachment(meeting_id, attachment_url, attachment_id=None):
    data = {"meeting_id": meeting_id, "attachment_url": attachment_url, "attachment_id": attachment_id}
    response = requests.post(f"{BASE_URL}/attachments", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error creating attachment: {response.text}"

def update_attachment(attachment_id, meeting_id, attachment_url):
    data = {"meeting_id": meeting_id, "attachment_url": attachment_url}
    response = requests.put(f"{BASE_URL}/attachments/{attachment_id}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error updating attachment {attachment_id}: {response.text}"

def delete_attachment(attachment_id):
    response = requests.delete(f"{BASE_URL}/attachments/{attachment_id}")
    if response.status_code == 204:
        return "Attachment deleted successfully"
    else:
        return f"Error deleting attachment {attachment_id}: {response.text}"


# Calendar Services
def get_all_calendars():
    response = requests.get(f"{BASE_URL}/calendars")
    if response.status_code == 200:
        calendars = response.json()
        for calendar in calendars:
            print(calendar)  # Print each calendar on a new line
    else:
        return f"Error fetching calendars: {response.text}"

def get_calendar_by_id(calendar_id):
    response = requests.get(f"{BASE_URL}/calendars/{calendar_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error fetching calendar {calendar_id}: {response.text}"

def create_calendar(title, details, calendar_id=None):
    data = {"title": title, "details": details, "calendar_id": calendar_id}
    response = requests.post(f"{BASE_URL}/calendars", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error creating calendar: {response.text}"

def update_calendar(calendar_id, title, details):
    data = {"title": title, "details": details}
    response = requests.put(f"{BASE_URL}/calendars/{calendar_id}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error updating calendar {calendar_id}: {response.text}"

def delete_calendar(calendar_id):
    response = requests.delete(f"{BASE_URL}/calendars/{calendar_id}")
    if response.status_code == 204:
        return "Calendar deleted successfully"
    else:
        return f"Error deleting calendar {calendar_id}: {response.text}"

def get_meetings_for_calendar(calendar_id):
    response = requests.get(f"{BASE_URL}/calendars/{calendar_id}/meetings")
    if response.status_code == 200:
        meetings = response.json()
        for meeting in meetings:
            print(meeting)  # Print each meeting on a new line
    else:
        return f"Error fetching meetings for calendar {calendar_id}: {response.text}"


# Meeting Services
def get_all_meetings():
    response = requests.get(f"{BASE_URL}/meetings")
    if response.status_code == 200:
        meetings = response.json()
        for meeting in meetings:
            print(meeting)  # Print each meeting on a new line
    else:
        return f"Error fetching meetings: {response.text}"

def get_meeting_by_id(meeting_id):
    response = requests.get(f"{BASE_URL}/meetings/{meeting_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error fetching meeting {meeting_id}: {response.text}"

def create_meeting(title, date_time, location, details, meeting_id=None):
    data = {"title": title, "date_time": date_time, "location": location, "details": details, "meeting_id": meeting_id}
    response = requests.post(f"{BASE_URL}/meetings", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error creating meeting: {response.text}"

def update_meeting(meeting_id, title, date_time, location, details):
    data = {"title": title, "date_time": date_time, "location": location, "details": details}
    response = requests.put(f"{BASE_URL}/meetings/{meeting_id}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error updating meeting {meeting_id}: {response.text}"

def delete_meeting(meeting_id):
    response = requests.delete(f"{BASE_URL}/meetings/{meeting_id}")
    if response.status_code == 204:
        return "Meeting deleted successfully"
    else:
        return f"Error deleting meeting {meeting_id}: {response.text}"

def link_participant_to_meeting(meeting_id, participant_id):
    response = requests.post(f"{BASE_URL}/meetings/{meeting_id}/participants/{participant_id}")
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error linking participant {participant_id} to meeting {meeting_id}: {response.text}"

def link_calendar_to_meeting(meeting_id, calendar_id):
    response = requests.post(f"{BASE_URL}/meetings/{meeting_id}/calendars/{calendar_id}")
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error linking calendar {calendar_id} to meeting {meeting_id}: {response.text}"

def get_participants_for_meeting(meeting_id):
    response = requests.get(f"{BASE_URL}/meetings/{meeting_id}/participants")
    if response.status_code == 200:
        participants = response.json()
        for participant in participants:
            print(participant)  # Print each participant on a new line
    else:
        return f"Error fetching participants for meeting {meeting_id}: {response.text}"


# Participant Services
def get_all_participants():
    response = requests.get(f"{BASE_URL}/participants")
    if response.status_code == 200:
        participants = response.json()
        for participant in participants:
            print(participant)  # Print each participant on a new line
    else:
        return f"Error fetching participants: {response.text}"

def get_participant_by_id(participant_id):
    response = requests.get(f"{BASE_URL}/participants/{participant_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error fetching participant {participant_id}: {response.text}"

def create_participant(name, email, participant_id=None):
    data = {"name": name, "email": email, "participant_id": participant_id}
    response = requests.post(f"{BASE_URL}/participants", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error creating participant: {response.text}"

def update_participant(participant_id, name, email):
    data = {"name": name, "email": email}
    response = requests.put(f"{BASE_URL}/participants/{participant_id}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error updating participant {participant_id}: {response.text}"

def delete_participant(participant_id):
    response = requests.delete(f"{BASE_URL}/participants/{participant_id}")
    if response.status_code == 204:
        return "Participant deleted successfully"
    else:
        return f"Error deleting participant {participant_id}: {response.text}"
