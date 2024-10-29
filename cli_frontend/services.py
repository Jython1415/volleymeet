import requests
import json
import random
import uuid
from datetime import datetime, timedelta
BASE_URL = "http://localhost:5001"  # Modify the base URL if backend is hosted elsewhere


# Helper function to create random string
def random_string(length):
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=length))

# Helper function to create invalid email
def random_invalid_email():
    return random_string(8)  # No "@" character

# Function to generate batch of meetings, participants, and attachments
def create_batch(batch_size=500):
    batch_data = {"meetings": []}
    
    for _ in range(batch_size):
        # Create a new meeting with potential errors
        meeting = {
            "meeting_id": str(uuid.uuid4()),
            "title": random_string(random.randint(20, 2500)),  # Potentially too long
            "date_time": (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %I:%M %p"),
            "location": random_string(random.randint(10, 2500)),  # Potentially too long
            "details": random_string(random.randint(20, 5000))
        }

        # Create participants
        participants = []
        for _ in range(random.randint(50, 100)):
            participant = {
                "participant_id": str(uuid.uuid4()),
                "meeting_id": meeting["meeting_id"],
                "name": random_string(random.randint(5, 650)),  # Potentially too long
                "email": random_invalid_email() if random.random() < 0.2 else f"{random_string(5)}@example.com"
            }
            participants.append(participant)

        # Create attachments
        attachments = []
        for _ in range(random.randint(5, 10)):
            url_prefix = "" if random.random() < 0.2 else "http://example.com/"
            attachment = {
                "attachment_id": str(uuid.uuid4()),
                "meeting_id": meeting["meeting_id"],
                "url": f"{url_prefix}{random_string(10)}.pdf"
            }
            attachments.append(attachment)

        meeting["participants"] = participants
        meeting["attachments"] = attachments
        batch_data["meetings"].append(meeting)

    # Save the batch to a JSON file
    with open("batch_data.json", "w") as file:
        json.dump(batch_data, file, indent=4)
    return "Batch of meetings, participants, and attachments created and saved to batch_data.json"

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
