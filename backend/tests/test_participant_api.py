import requests
import json
from models.global_functions_sql import generate_uuid

BACKEND_BASE_URL = "http://localhost:5001/participants"


def test_get_all_participants():
    response = requests.get(BACKEND_BASE_URL)
    if response.status_code == 200:
        print("GET /participants: Success")
        print(json.dumps(response.json(), indent=4))
    elif response.status_code == 404:
        print("GET /participants: No participants found")
    else:
        print(f"GET /participants: Failed with status code {response.status_code}")


def test_get_participant(participant_id):
    response = requests.get(f"{BACKEND_BASE_URL}/{participant_id}")
    if response.status_code == 200:
        print(f"GET /participants/{participant_id}: Success")
        print(json.dumps(response.json(), indent=4))
    elif response.status_code == 404:
        print(f"GET /participants/{participant_id}: Participant not found")
    else:
        print(
            f"GET /participants/{participant_id}: Failed with status code {response.status_code}"
        )


def test_create_participant_no_uuid():
    participant_data = {
        "name": "Alice Doe",
        "email": "alice@example.com",
    }
    response = requests.post(BACKEND_BASE_URL, json=participant_data)
    if response.status_code == 201:
        print("POST /participants: Success")
    elif response.status_code == 400:
        print(f"POST /participants: Failed with error: {response.json().get('error')}")
    else:
        print(f"POST /participants: Failed with status code {response.status_code}")


def test_create_participant_uuid(participant_id):
    participant_data = {
        "name": "Bob Smith",
        "email": "bob@example.com",
        "participant_id": str(participant_id),
    }
    response = requests.post(BACKEND_BASE_URL, json=participant_data)
    if response.status_code == 201:
        print("POST /participants: Success")
    elif response.status_code == 400:
        print(f"POST /participants: Failed with error: {response.json().get('error')}")
    else:
        print(f"POST /participants: Failed with status code {response.status_code}")


def test_update_participant(participant_id):
    updated_data = {
        "name": "Bob Johnson",
        "email": "bob.johnson@example.com",
    }
    response = requests.put(f"{BACKEND_BASE_URL}/{participant_id}", json=updated_data)
    if response.status_code == 200:
        print(f"PUT /participants/{participant_id}: Success")
    elif response.status_code == 400:
        print(
            f"PUT /participants/{participant_id}: Failed with error: {response.json().get('error')}"
        )
    else:
        print(
            f"PUT /participants/{participant_id}: Failed with status code {response.status_code}"
        )


def test_delete_participant(participant_id):
    response = requests.delete(f"{BACKEND_BASE_URL}/{participant_id}")
    if response.status_code == 204:
        print(f"DELETE /participants/{participant_id}: Success")
    elif response.status_code == 404:
        print(f"DELETE /participants/{participant_id}: Participant not found")
    else:
        print(
            f"DELETE /participants/{participant_id}: Failed with status code {response.status_code}"
        )


def main():
    # Run tests for the API
    print("Testing GET all participants:")
    test_get_all_participants()

    print("\nTesting POST create participant with no UUID:")
    test_create_participant_no_uuid()

    print("\nTesting GET all participants after creation:")
    test_get_all_participants()

    participant_id = generate_uuid()
    print(f"\nTesting POST create participant with a specified UUID: {participant_id}")
    test_create_participant_uuid(participant_id)

    print("\nTesting GET one participant:")
    test_get_participant(participant_id)

    print("\nTesting Update participant:")
    test_update_participant(participant_id)

    print("\nTesting GET updated participant:")
    test_get_participant(participant_id)

    nonexist_participant_id = generate_uuid()
    print("\nTesting Update participant that doesn't exist:")
    test_update_participant(nonexist_participant_id)

    print("\nTesting DELETE participant:")
    test_delete_participant(participant_id)

    print("\nTesting GET deleted participant (should be not found):")
    test_get_participant(participant_id)


if __name__ == "__main__":
    main()
