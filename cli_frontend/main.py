import random
from services import (
    get_all_attachments, get_attachment_by_id, create_attachment, update_attachment, delete_attachment,
    get_all_calendars, get_calendar_by_id, create_calendar, update_calendar, delete_calendar, get_meetings_for_calendar,
    get_all_meetings, get_meeting_by_id, create_meeting, update_meeting, delete_meeting,
    link_participant_to_meeting, link_calendar_to_meeting, get_participants_for_meeting,
    get_all_participants, get_participant_by_id, create_participant, update_participant, delete_participant, create_batch, send_batch_data
)

def print_main_menu():
    print("\n==== Main Menu ====")
    print("1. Manage Attachments")
    print("2. Manage Calendars")
    print("3. Manage Meetings")
    print("4. Manage Participants")
    print("9. Create Batch Request")
    print("0. Exit")


def print_attachment_menu():
    print("\n==== Attachment Menu ====")
    print("1. Get All Attachments")
    print("2. Get Attachment by ID")
    print("3. Create Attachment")
    print("4. Update Attachment")
    print("5. Delete Attachment")
    print("0. Back to Main Menu")


def print_calendar_menu():
    print("\n==== Calendar Menu ====")
    print("1. Get All Calendars")
    print("2. Get Calendar by ID")
    print("3. Create Calendar")
    print("4. Update Calendar")
    print("5. Delete Calendar")
    print("6. Get Meetings for a Calendar")
    print("0. Back to Main Menu")


def print_meeting_menu():
    print("\n==== Meeting Menu ====")
    print("1. Get All Meetings")
    print("2. Get Meeting by ID")
    print("3. Create Meeting")
    print("4. Update Meeting")
    print("5. Delete Meeting")
    print("6. Link Participant to Meeting")
    print("7. Link Calendar to Meeting")
    print("8. Get Participants for a Meeting")
    print("0. Back to Main Menu")


def print_participant_menu():
    print("\n==== Participant Menu ====")
    print("1. Get All Participants")
    print("2. Get Participant by ID")
    print("3. Create Participant")
    print("4. Update Participant")
    print("5. Delete Participant")
    print("0. Back to Main Menu")


def create_batch_data():
    print("Creating batch of meetings, participants, and attachments...")
    result = create_batch(batch_size=random.randint(500, 1000))
    print(result)

def handle_attachments():
    while True:
        print_attachment_menu()
        choice = input("Select an option: ")

        if choice == "1":
            print(get_all_attachments())
        elif choice == "2":
            attachment_id = input("Enter Attachment ID: ")
            print(get_attachment_by_id(attachment_id))
        elif choice == "3":
            meeting_id = input("Enter Meeting ID: ")
            attachment_url = input("Enter Attachment URL: ")
            attachment_id = input("Enter Attachment ID (optional, leave blank for auto-generated): ")
            if not attachment_id:
                attachment_id = None
            print(create_attachment(meeting_id, attachment_url, attachment_id))
        elif choice == "4":
            attachment_id = input("Enter Attachment ID: ")
            meeting_id = input("Enter Meeting ID: ")
            attachment_url = input("Enter Attachment URL: ")
            print(update_attachment(attachment_id, meeting_id, attachment_url))
        elif choice == "5":
            attachment_id = input("Enter Attachment ID: ")
            print(delete_attachment(attachment_id))
        elif choice == "0":
            break
        else:
            print("Invalid option, try again.")


def handle_calendars():
    while True:
        print_calendar_menu()
        choice = input("Select an option: ")

        if choice == "1":
            print(get_all_calendars())
        elif choice == "2":
            calendar_id = input("Enter Calendar ID: ")
            print(get_calendar_by_id(calendar_id))
        elif choice == "3":
            title = input("Enter Calendar Title: ")
            details = input("Enter Calendar Details: ")
            calendar_id = input("Enter Calendar ID (optional, leave blank for auto-generated): ")
            if not calendar_id:
                calendar_id = None
            print(create_calendar(title, details, calendar_id))
        elif choice == "4":
            calendar_id = input("Enter Calendar ID: ")
            title = input("Enter Calendar Title: ")
            details = input("Enter Calendar Details: ")
            print(update_calendar(calendar_id, title, details))
        elif choice == "5":
            calendar_id = input("Enter Calendar ID: ")
            print(delete_calendar(calendar_id))
        elif choice == "6":
            calendar_id = input("Enter Calendar ID: ")
            print(get_meetings_for_calendar(calendar_id))
        elif choice == "0":
            break
        else:
            print("Invalid option, try again.")


def handle_meetings():
    while True:
        print_meeting_menu()
        choice = input("Select an option: ")

        if choice == "1":
            print(get_all_meetings())
        elif choice == "2":
            meeting_id = input("Enter Meeting ID: ")
            print(get_meeting_by_id(meeting_id))
        elif choice == "3":
            title = input("Enter Meeting Title: ")
            date_time = input("Enter Date and Time (YYYY-MM-DD HH:MM AM/PM): ")
            location = input("Enter Location: ")
            details = input("Enter Details: ")
            meeting_id = input("Enter Meeting ID (optional, leave blank for auto-generated): ")
            if not meeting_id:
                meeting_id = None
            print(create_meeting(title, date_time, location, details, meeting_id))
        elif choice == "4":
            meeting_id = input("Enter Meeting ID: ")
            title = input("Enter Meeting Title: ")
            date_time = input("Enter Date and Time (YYYY-MM-DD HH:MM AM/PM): ")
            location = input("Enter Location: ")
            details = input("Enter Details: ")
            print(update_meeting(meeting_id, title, date_time, location, details))
        elif choice == "5":
            meeting_id = input("Enter Meeting ID: ")
            print(delete_meeting(meeting_id))
        elif choice == "6":
            meeting_id = input("Enter Meeting ID: ")
            participant_id = input("Enter Participant ID: ")
            print(link_participant_to_meeting(meeting_id, participant_id))
        elif choice == "7":
            meeting_id = input("Enter Meeting ID: ")
            calendar_id = input("Enter Calendar ID: ")
            print(link_calendar_to_meeting(meeting_id, calendar_id))
        elif choice == "8":
            meeting_id = input("Enter Meeting ID: ")
            print(get_participants_for_meeting(meeting_id))
        elif choice == "0":
            break
        else:
            print("Invalid option, try again.")


def handle_participants():
    while True:
        print_participant_menu()
        choice = input("Select an option: ")

        if choice == "1":
            print(get_all_participants())
        elif choice == "2":
            participant_id = input("Enter Participant ID: ")
            print(get_participant_by_id(participant_id))
        elif choice == "3":
            name = input("Enter Participant Name: ")
            email = input("Enter Participant Email: ")
            participant_id = input("Enter Participant ID (optional, leave blank for auto-generated): ")
            if not participant_id:
                participant_id = None
            print(create_participant(name, email, participant_id))
        elif choice == "4":
            participant_id = input("Enter Participant ID: ")
            name = input("Enter Participant Name: ")
            email = input("Enter Participant Email: ")
            print(update_participant(participant_id, name, email))
        elif choice == "5":
            participant_id = input("Enter Participant ID: ")
            print(delete_participant(participant_id))
        elif choice == "0":
            break
        else:
            print("Invalid option, try again.")


def create_and_send_batch_data():
    print("Creating and sending batch of meetings, participants, and attachments...")
    batch_data = create_batch(batch_size=random.randint(500, 1000), invalid_percentage=20)
    result = send_batch_data(batch_data)
    print(result)

# Update main function to include the new batch sending option
def main():
    while True:
        print_main_menu()
        choice = input("Select an option: ")

        if choice == "1":
            handle_attachments()
        elif choice == "2":
            handle_calendars()
        elif choice == "3":
            handle_meetings()
        elif choice == "4":
            handle_participants()
        elif choice == "9":
            create_and_send_batch_data()  # Updated to create and send the batch
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option, try again.")
if __name__ == "__main__":
    main()