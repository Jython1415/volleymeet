import argparse
from volleymeet.db import (
    initialize_database,
    add_meeting,
    delete_meeting,
    add_participant,
    delete_participant,
    add_calendar,
    delete_calendar,
    add_attachment,
    delete_attachment,
    list_participants_for_meeting,
    list_attachments_for_meeting,
    list_calendars_for_meeting,
    list_meetings_in_calendar,
    list_meetings_for_participant,
    list_all_meetings,
    list_all_participants,
    list_all_calendars,
    add_participant_to_meeting,
    schedule_meeting_in_calendar,
)


def create_cli():
    """Creates the CLI for managing meetings, participants, calendars, and attachments."""
    parser = argparse.ArgumentParser(description="Manage volleyball meetings")

    subparsers = parser.add_subparsers(title="commands", dest="command")

    # --- Meetings Subcommands ---
    meeting_parser = subparsers.add_parser("meeting", help="Manage meetings")
    meeting_subparsers = meeting_parser.add_subparsers(
        title="meeting commands", dest="subcommand"
    )

    # Add meeting
    add_meeting_parser = meeting_subparsers.add_parser("add", help="Add a new meeting")
    add_meeting_parser.add_argument(
        "--title", required=True, help="Title of the meeting"
    )
    add_meeting_parser.add_argument(
        "--details", required=False, help="Details of the meeting"
    )
    add_meeting_parser.add_argument(
        "--location", required=False, help="Location of the meeting"
    )
    add_meeting_parser.add_argument(
        "--date-time",
        required=True,
        help="Date and time of the meeting (YYYY-MM-DD HH:MM AM/PM)",
    )

    # List meetings
    list_meeting_parser = meeting_subparsers.add_parser(
        "list", help="List all meetings"
    )

    # Delete meeting
    delete_meeting_parser = meeting_subparsers.add_parser(
        "delete", help="Delete a meeting by ID"
    )
    delete_meeting_parser.add_argument(
        "--id", required=True, help="ID of the meeting to delete"
    )

    # Add participant to meeting
    add_participant_to_meeting_parser = meeting_subparsers.add_parser(
        "add-participant", help="Add a participant to a meeting"
    )
    add_participant_to_meeting_parser.add_argument(
        "--meeting-id", required=True, help="ID of the meeting"
    )
    add_participant_to_meeting_parser.add_argument(
        "--participant-id", required=True, help="ID of the participant"
    )

    # List participants in a meeting
    list_meeting_participants_parser = meeting_subparsers.add_parser(
        "list-participants", help="List participants for a meeting"
    )
    list_meeting_participants_parser.add_argument(
        "--meeting-id", required=True, help="ID of the meeting"
    )

    # Schedule meeting in calendar
    schedule_meeting_parser = meeting_subparsers.add_parser(
        "schedule", help="Schedule a meeting in a calendar"
    )
    schedule_meeting_parser.add_argument(
        "--meeting-id", required=True, help="ID of the meeting"
    )
    schedule_meeting_parser.add_argument(
        "--calendar-id", required=True, help="ID of the calendar"
    )

    # --- Participants Subcommands ---
    participant_parser = subparsers.add_parser(
        "participant", help="Manage participants"
    )
    participant_subparsers = participant_parser.add_subparsers(
        title="participant commands", dest="subcommand"
    )

    # Add participant
    add_participant_parser = participant_subparsers.add_parser(
        "add", help="Add a new participant"
    )
    add_participant_parser.add_argument(
        "--name", required=True, help="Name of the participant"
    )
    add_participant_parser.add_argument(
        "--email", required=True, help="Email of the participant"
    )

    # List participants
    list_participants_parser = participant_subparsers.add_parser(
        "list", help="List all participants"
    )

    # Delete participant
    delete_participant_parser = participant_subparsers.add_parser(
        "delete", help="Delete a participant by ID"
    )
    delete_participant_parser.add_argument(
        "--id", required=True, help="ID of the participant to delete"
    )

    # --- Calendars Subcommands ---
    calendar_parser = subparsers.add_parser("calendar", help="Manage calendars")
    calendar_subparsers = calendar_parser.add_subparsers(
        title="calendar commands", dest="subcommand"
    )

    # Add calendar
    add_calendar_parser = calendar_subparsers.add_parser(
        "add", help="Add a new calendar"
    )
    add_calendar_parser.add_argument(
        "--title", required=True, help="Title of the calendar"
    )
    add_calendar_parser.add_argument(
        "--details", required=False, help="Details of the calendar"
    )

    # List calendars
    list_calendars_parser = calendar_subparsers.add_parser(
        "list", help="List all calendars"
    )

    # Delete calendar
    delete_calendar_parser = calendar_subparsers.add_parser(
        "delete", help="Delete a calendar by ID"
    )
    delete_calendar_parser.add_argument(
        "--id", required=True, help="ID of the calendar to delete"
    )

    # --- Attachments Subcommands ---
    attachment_parser = subparsers.add_parser("attachment", help="Manage attachments")
    attachment_subparsers = attachment_parser.add_subparsers(
        title="attachment commands", dest="subcommand"
    )

    # Add attachment
    add_attachment_parser = attachment_subparsers.add_parser(
        "add", help="Add an attachment to a meeting"
    )
    add_attachment_parser.add_argument(
        "--meeting-id", required=True, help="ID of the meeting"
    )
    add_attachment_parser.add_argument(
        "--url", required=True, help="URL of the attachment"
    )

    # List attachments for a meeting
    list_attachments_parser = attachment_subparsers.add_parser(
        "list", help="List attachments for a meeting"
    )
    list_attachments_parser.add_argument(
        "--meeting-id", required=True, help="ID of the meeting"
    )

    # Delete attachment
    delete_attachment_parser = attachment_subparsers.add_parser(
        "delete", help="Delete an attachment by ID"
    )
    delete_attachment_parser.add_argument(
        "--id", required=True, help="ID of the attachment to delete"
    )

    return parser


def main():
    """Entry point for the CLI."""
    initialize_database()  # Ensure the database is initialized before any command

    parser = create_cli()
    args = parser.parse_args()

    # Handle meetings
    if args.command == "meeting":
        if args.subcommand == "add":
            add_meeting(args.title, args.details, args.location, args.date_time)
            print(f"Meeting '{args.title}' added.")

        elif args.subcommand == "list":
            meetings = list_all_meetings()
            for meeting in meetings:
                print(
                    f"ID: {meeting['meeting_id']}, Title: {meeting['title']}, Date: {meeting['date_time']}"
                )

        elif args.subcommand == "delete":
            delete_meeting(args.id)
            print(f"Meeting with ID {args.id} deleted.")

        elif args.subcommand == "add-participant":
            add_participant_to_meeting(args.meeting_id, args.participant_id)
            print(
                f"Participant with ID {args.participant_id} added to meeting {args.meeting_id}."
            )

        elif args.subcommand == "list-participants":
            participants = list_participants_for_meeting(args.meeting_id)
            print(f"Participants for meeting {args.meeting_id}: {participants}")

        elif args.subcommand == "schedule":
            schedule_meeting_in_calendar(args.meeting_id, args.calendar_id)
            print(
                f"Meeting {args.meeting_id} scheduled in calendar {args.calendar_id}."
            )

    # Handle participants
    elif args.command == "participant":
        if args.subcommand == "add":
            add_participant(args.name, args.email)
            print(f"Participant '{args.name}' added.")

        elif args.subcommand == "list":
            participants = list_all_participants()
            for participant in participants:
                print(
                    f"ID: {participant['participant_id']}, Name: {participant['name']}, Email: {participant['email']}"
                )

        elif args.subcommand == "delete":
            delete_participant(args.id)
            print(f"Participant with ID {args.id} deleted.")

    # Handle calendars
    elif args.command == "calendar":
        if args.subcommand == "add":
            add_calendar(args.title, args.details)
            print(f"Calendar '{args.title}' added.")

        elif args.subcommand == "list":
            calendars = list_all_calendars()
            for calendar in calendars:
                print(
                    f"ID: {calendar['calendar_id']}, Title: {calendar['title']}, Details: {calendar['details']}"
                )

        elif args.subcommand == "delete":
            delete_calendar(args.id)
            print(f"Calendar with ID {args.id} deleted.")

    # Handle attachments
    elif args.command == "attachment":
        if args.subcommand == "add":
            add_attachment(args.meeting_id, args.url)
            print(f"Attachment '{args.url}' added to meeting {args.meeting_id}.")

        elif args.subcommand == "list":
            attachments = list_attachments_for_meeting(args.meeting_id)
            print(f"Attachments for meeting {args.meeting_id}: {attachments}")

        elif args.subcommand == "delete":
            delete_attachment(args.id)
            print(f"Attachment with ID {args.id} deleted.")


if __name__ == "__main__":
    main()
