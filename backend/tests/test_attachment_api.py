import requests
import json
from models.global_functions_sql import generate_uuid

BACKEND_BASE_URL = "http://localhost:5001/attachments"


def test_get_all_attachments():
    response = requests.get(BACKEND_BASE_URL)
    if response.status_code == 200:
        print("GET /attachments: Success")
        print(json.dumps(response.json(), indent=4))
    elif response.status_code == 404:
        print("GET /attachments: No attachments found")
    else:
        print(f"GET /attachments: Failed with status code {response.status_code}")


def test_get_attachment(attachment_id):
    response = requests.get(f"{BACKEND_BASE_URL}/{attachment_id}")
    if response.status_code == 200:
        print(f"GET /attachments/{attachment_id}: Success")
        print(json.dumps(response.json(), indent=4))
    elif response.status_code == 404:
        print(f"GET /attachments/{attachment_id}: Attachment not found")
    else:
        print(
            f"GET /attachments/{attachment_id}: Failed with status code {response.status_code}"
        )


def test_create_attachment_no_uuid():
    attachment_data = {
        "meeting_id": "da19c67e-839d-11ef-9c56-0242ac120002",
        "attachment_url": "http://example.com/test_attachment",
    }
    response = requests.post(BACKEND_BASE_URL, json=attachment_data)
    if response.status_code == 201:
        print("POST /attachments: Success")
    elif response.status_code == 400:
        print(f"POST /attachments: Failed with error: {response.json().get('error')}")
    else:
        print(f"POST /attachments: Failed with status code {response.status_code}")


def test_create_attachment_uuid(attachment_id):
    attachment_data = {
        "meeting_id": "da19c67e-839d-11ef-9c56-0242ac120002",
        "attachment_url": "http://example.com/test_attachment",
        "attachment_id": str(attachment_id),
    }
    response = requests.post(BACKEND_BASE_URL, json=attachment_data)
    if response.status_code == 201:
        print("POST /attachments: Success")
    elif response.status_code == 400:
        print(f"POST /attachments: Failed with error: {response.json().get('error')}")
    else:
        print(f"POST /attachments: Failed with status code {response.status_code}")


def test_update_attachment(attachment_id):
    updated_data = {
        "meeting_id": "da19c67e-839d-11ef-9c56-0242ac120002",
        "attachment_url": "http://example.com/updated_attachment",
    }
    response = requests.put(f"{BACKEND_BASE_URL}/{attachment_id}", json=updated_data)
    if response.status_code == 200:
        print(f"PUT /attachments/{attachment_id}: Success")
    elif response.status_code == 400:
        print(
            f"PUT /attachments/{attachment_id}: Failed with error: {response.json().get('error')}"
        )
    else:
        print(
            f"PUT /attachments/{attachment_id}: Failed with status code {response.status_code}"
        )


def test_delete_attachment(attachment_id):
    response = requests.delete(f"{BACKEND_BASE_URL}/{attachment_id}")
    if response.status_code == 204:
        print(f"DELETE /attachments/{attachment_id}: Success")
    elif response.status_code == 404:
        print(f"DELETE /attachments/{attachment_id}: Attachment not found")
    else:
        print(
            f"DELETE /attachments/{attachment_id}: Failed with status code {response.status_code}"
        )


def main():
    # Run tests for the API
    print("Testing GET all attachments:")
    test_get_all_attachments()

    print("\nTesting POST create attachment with no uuid:")
    test_create_attachment_no_uuid()

    print("\nTesting GET all attachments after creation:")
    test_get_all_attachments()

    attachment_id = generate_uuid()
    print(f"\nTesting POST create attachment with a specified uuid: {attachment_id}")
    test_create_attachment_uuid(attachment_id)

    print("\nTesting GET one attachment:")
    test_get_attachment(attachment_id)

    print("\nTesting Update attachment:")
    test_update_attachment(attachment_id)

    print("\nTesting GET updated attachment:")
    test_get_attachment(attachment_id)

    print("\nTesting DELETE attachment:")
    test_delete_attachment(attachment_id)

    print("\nTesting GET deleted attachment (should be not found):")
    test_get_attachment(attachment_id)


if __name__ == "__main__":
    main()
