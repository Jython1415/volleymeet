import requests
import json
from models.global_functions_sql import generate_uuid

BACKEND_BASE_URL = "http://localhost:5001/calendars"


def test_get_all_calendars():
    response = requests.get(BACKEND_BASE_URL)
    if response.status_code == 200:
        print("GET /calendars: Success")
        print(json.dumps(response.json(), indent=4))
    elif response.status_code == 404:
        print("GET /calendars: No calendars found")
    else:
        print(f"GET /calendars: Failed with status code {response.status_code}")


def test_get_calendar(calendar_id):
    response = requests.get(f"{BACKEND_BASE_URL}/{calendar_id}")
    if response.status_code == 200:
        print(f"GET /calendars/{calendar_id}: Success")
        print(json.dumps(response.json(), indent=4))
    elif response.status_code == 404:
        print(f"GET /calendars/{calendar_id}: Calendar not found")
    else:
        print(
            f"GET /calendars/{calendar_id}: Failed with status code {response.status_code}"
        )


def test_create_calendar_no_uuid():
    calendar_data = {
        "title": "New Calendar",
        "details": "Details about the new calendar",
    }
    response = requests.post(BACKEND_BASE_URL, json=calendar_data)
    if response.status_code == 201:
        print("POST /calendars: Success")
    elif response.status_code == 400:
        print(f"POST /calendars: Failed with error: {response.json().get('error')}")
    else:
        print(f"POST /calendars: Failed with status code {response.status_code}")


def test_create_calendar_uuid(calendar_id):
    calendar_data = {
        "title": "New Calendar",
        "details": "Details about the new calendar",
        "calendar_id": str(calendar_id),
    }
    response = requests.post(BACKEND_BASE_URL, json=calendar_data)
    if response.status_code == 201:
        print("POST /calendars: Success")
    elif response.status_code == 400:
        print(f"POST /calendars: Failed with error: {response.json().get('error')}")
    else:
        print(f"POST /calendars: Failed with status code {response.status_code}")


def test_update_calendar(calendar_id):
    updated_data = {
        "title": "Updated Calendar",
        "details": "Updated details of the calendar",
    }
    response = requests.put(f"{BACKEND_BASE_URL}/{calendar_id}", json=updated_data)
    if response.status_code == 200:
        print(f"PUT /calendars/{calendar_id}: Success")
    elif response.status_code == 400:
        print(
            f"PUT /calendars/{calendar_id}: Failed with error: {response.json().get('error')}"
        )
    else:
        print(
            f"PUT /calendars/{calendar_id}: Failed with status code {response.status_code}"
        )


def test_delete_calendar(calendar_id):
    response = requests.delete(f"{BACKEND_BASE_URL}/{calendar_id}")
    if response.status_code == 204:
        print(f"DELETE /calendars/{calendar_id}: Success")
    elif response.status_code == 404:
        print(f"DELETE /calendars/{calendar_id}: Calendar not found")
    else:
        print(
            f"DELETE /calendars/{calendar_id}: Failed with status code {response.status_code}"
        )


def main():
    # Run tests for the API
    print("Testing GET all calendars:")
    test_get_all_calendars()

    print("\nTesting POST create calendar with no uuid:")
    test_create_calendar_no_uuid()

    print("\nTesting GET all calendars after creation:")
    test_get_all_calendars()

    calendar_id = generate_uuid()
    print("\nTesting POST create calendar with a specified uuid:")
    test_create_calendar_uuid(calendar_id)

    print("\nTesting GET one calendar:")
    test_get_calendar(calendar_id)

    print("\nTesting Update calendar:")
    test_update_calendar(calendar_id)

    print("\nTesting GET updated calendar:")
    test_get_calendar(calendar_id)

    print("\nTesting DELETE calendar:")
    test_delete_calendar(calendar_id)

    print("\nTesting GET deleted calendar (should be not found):")
    test_get_calendar(calendar_id)


if __name__ == "__main__":
    main()
