import requests

ATTACHMENT_BASE_URL = "http://localhost:5001"
CALENDAR_BASE_URL = "http://localhost:5002"
MEETING_BASE_URL = "http://localhost:5004"
PARTICIPANT_BASE_URL = "http://localhost:5005"

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
