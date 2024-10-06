import requests
import time
import json
from global_functions_sql import generate_uuid


BACKEND_BASE_URL = "http://localhost:5001/meetings"


def test_get_all_meetings():
    response = requests.get(BACKEND_BASE_URL)
    if response.status_code == 200:
        print("GET /meetings: Success")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"GET /meetings: Failed with status code {response.status_code}")


def test_get_meeting(meeting_id):
    response = requests.get(f"{BACKEND_BASE_URL}/{meeting_id}")
    if response.status_code == 200:
        print(f"GET /meetings/{meeting_id}: Success")
        print(json.dumps(response.json(), indent=4))
    else:
        print(
            f"GET /meetings/{meeting_id}: Failed with status code {response.status_code}"
        )


def test_create_meeting_no_uuid():
    meeting_data = {
        "title": "New Meeting",
        "date_time": "2024-10-10 10:00:00",
        "location": "Conference Room",
        "details": "Discussion on project updates",
    }
    response = requests.post(BACKEND_BASE_URL, json=meeting_data)
    if response.status_code == 201:
        print("POST /meetings: Success")
    else:
        print(f"POST /meetings: Failed with status code {response.status_code}")


def test_create_meeting_uuid(meeting_id):
    meeting_data = {
        "title": "New Meeting",
        "date_time": "2024-10-10 10:00:00",
        "location": "Conference Room",
        "details": "Discussion on project updates",
        "meeting_id": str(meeting_id),
    }
    response = requests.post(BACKEND_BASE_URL, json=meeting_data)
    if response.status_code == 201:
        print("POST /meetings: Success")
    else:
        print(f"POST /meetings: Failed with status code {response.status_code}")


def test_update_meeting(meeting_id):
    updated_data = {
        "title": "Updated Meeting",
        "date_time": "2024-10-12 11:00:00",
        "location": "Updated Location",
        "details": "Updated details of the meeting",
    }
    response = requests.put(f"{BACKEND_BASE_URL}/{meeting_id}", json=updated_data)
    if response.status_code == 200:
        print(f"PUT /meetings/{meeting_id}: Success")
    else:
        print(
            f"PUT /meetings/{meeting_id}: Failed with status code {response.status_code}"
        )


def test_delete_meeting(meeting_id):
    response = requests.delete(f"{BACKEND_BASE_URL}/{meeting_id}")
    if response.status_code == 204:
        print(f"DELETE /meetings/{meeting_id}: Success")
    else:
        print(
            f"DELETE /meetings/{meeting_id}: Failed with status code {response.status_code}"
        )


def main():
    # Run tests for the API
    print("Testing GET all meetings:")
    test_get_all_meetings()

    print("\nTesting POST create meeting with no uuid:")
    test_create_meeting_no_uuid()

    print("Testing GET all meetings:")
    test_get_all_meetings()

    meeting_id = generate_uuid()
    print("\nTesting POST create meeting with a specified uuid:")
    test_create_meeting_uuid(meeting_id)

    print("Testing GET all meetings:")
    test_get_all_meetings()

    time.sleep(5)
    print("Testing GET one meeting:")
    test_get_meeting(meeting_id)

    time.sleep(1)
    print("Testing Update meeting:")
    test_update_meeting(meeting_id)

    print("Testing GET all meetings:")
    test_get_all_meetings()

    time.sleep(5)
    print("Testing GET updated meeting:")
    test_get_meeting(meeting_id)

    time.sleep(1)
    print("Test deleting a meeting")
    test_delete_meeting(meeting_id)

    print("Testing GET deleted meeting (should be an meeting not found):")
    test_get_meeting(meeting_id)

    print("Testing GET all meetings:")
    test_get_all_meetings()


if __name__ == "__main__":
    main()
