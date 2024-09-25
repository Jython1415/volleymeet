import argparse

from volleymeet.meetings import create_meeting, update_meeting, delete_meeting
from volleymeet.calendars import (
    create_calendar,
    update_calendar,
    delete_calendar,
)
from volleymeet.participants import (
    create_participant,
    update_participant,
    delete_participant,
)
from volleymeet.attachments import (
    create_attachment,
    update_attachment,
    delete_attachment,
)


def create_cli():
    parser = argparse.ArgumentParser(
        description="CLI for managing meetings, calendars, participants, and attachments."
    )
    subparsers = parser.add_subparsers(title="Commands", help="Available commands")

    # Meetings
    meeting_parser = subparsers.add_parser("meeting", help="Manage meetings")
    meeting_subparsers = meeting_parser.add_subparsers(title="Meeting Commands")

    create_meeting_parser = meeting_subparsers.add_parser(
        "create", help="Create a new meeting"
    )
    create_meeting_parser.add_argument(
        "--title", required=True, help="Title of the meeting"
    )
    create_meeting_parser.add_argument(
        "--datetime",
        required=True,
        help="Date and time of the meeting (YYYY-MM-DD HH:MM AM/PM)",
    )
    create_meeting_parser.add_argument(
        "--location", required=False, help="Location of the meeting"
    )
    create_meeting_parser.add_argument(
        "--details", required=False, help="Details of the meeting"
    )
    create_meeting_parser.set_defaults(func=create_meeting)

    update_meeting_parser = meeting_subparsers.add_parser(
        "update", help="Update an existing meeting"
    )
    update_meeting_parser.add_argument("--id", required=True, help="ID of the meeting")
    update_meeting_parser.add_argument(
        "--title", required=True, help="New title of the meeting"
    )
    update_meeting_parser.add_argument(
        "--datetime", required=False, help="New date and time of the meeting"
    )
    update_meeting_parser.add_argument(
        "--location", required=False, help="New location of the meeting"
    )
    update_meeting_parser.add_argument(
        "--details", required=False, help="New details of the meeting"
    )
    update_meeting_parser.set_defaults(func=update_meeting)

    delete_meeting_parser = meeting_subparsers.add_parser(
        "delete", help="Delete a meeting"
    )
    delete_meeting_parser.add_argument("--id", required=True, help="ID of the meeting")
    delete_meeting_parser.set_defaults(func=delete_meeting)

    # Calendars
    calendar_parser = subparsers.add_parser("calendar", help="Manage calendars")
    calendar_subparsers = calendar_parser.add_subparsers(title="Calendar Commands")

    create_calendar_parser = calendar_subparsers.add_parser(
        "create", help="Create a new calendar"
    )
    create_calendar_parser.add_argument(
        "--title", required=True, help="Title of the calendar"
    )
    create_calendar_parser.add_argument(
        "--details", required=False, help="Details of the calendar"
    )
    create_calendar_parser.set_defaults(func=create_calendar)

    update_calendar_parser = calendar_subparsers.add_parser(
        "update", help="Update an existing calendar"
    )
    update_calendar_parser.add_argument(
        "--id", required=True, help="ID of the calendar"
    )
    update_calendar_parser.add_argument(
        "--title", required=True, help="New title of the calendar"
    )
    update_calendar_parser.add_argument(
        "--details", required=False, help="New details of the calendar"
    )
    update_calendar_parser.set_defaults(func=update_calendar)

    delete_calendar_parser = calendar_subparsers.add_parser(
        "delete", help="Delete a calendar"
    )
    delete_calendar_parser.add_argument(
        "--id", required=True, help="ID of the calendar"
    )
    delete_calendar_parser.set_defaults(func=delete_calendar)

    # Participants
    participant_parser = subparsers.add_parser(
        "participant", help="Manage participants"
    )
    participant_subparsers = participant_parser.add_subparsers(
        title="Participant Commands"
    )

    create_participant_parser = participant_subparsers.add_parser(
        "create", help="Create a new participant"
    )
    create_participant_parser.add_argument(
        "--name", required=True, help="Name of the participant"
    )
    create_participant_parser.add_argument(
        "--meeting_id", required=True, help="ID of the meeting"
    )
    create_participant_parser.add_argument(
        "--email", required=True, help="Email of the participant"
    )
    create_participant_parser.set_defaults(func=create_participant)

    update_participant_parser = participant_subparsers.add_parser(
        "update", help="Update an existing participant"
    )
    update_participant_parser.add_argument(
        "--id", required=True, help="ID of the participant"
    )
    update_participant_parser.add_argument(
        "--name", required=False, help="New name of the participant"
    )
    update_participant_parser.add_argument(
        "--email", required=False, help="New email of the participant"
    )
    update_participant_parser.set_defaults(func=update_participant)

    delete_participant_parser = participant_subparsers.add_parser(
        "delete", help="Delete a participant"
    )
    delete_participant_parser.add_argument(
        "--id", required=True, help="ID of the participant"
    )
    delete_participant_parser.set_defaults(func=delete_participant)

    # Attachments
    attachment_parser = subparsers.add_parser("attachment", help="Manage attachments")
    attachment_subparsers = attachment_parser.add_subparsers(
        title="Attachment Commands"
    )

    create_attachment_parser = attachment_subparsers.add_parser(
        "create", help="Create a new attachment"
    )
    create_attachment_parser.add_argument(
        "--url", required=True, help="URL of the attachment"
    )
    create_attachment_parser.add_argument(
        "--meeting_id", required=True, help="ID of the meeting"
    )
    create_attachment_parser.set_defaults(func=create_attachment)

    update_attachment_parser = attachment_subparsers.add_parser(
        "update", help="Update an existing attachment"
    )
    update_attachment_parser.add_argument(
        "--id", required=True, help="ID of the attachment"
    )
    update_attachment_parser.add_argument(
        "--url", required=False, help="New URL of the attachment"
    )
    update_attachment_parser.set_defaults(func=update_attachment)

    delete_attachment_parser = attachment_subparsers.add_parser(
        "delete", help="Delete an attachment"
    )
    delete_attachment_parser.add_argument(
        "--id", required=True, help="ID of the attachment"
    )
    delete_attachment_parser.set_defaults(func=delete_attachment)

    return parser


def main():
    parser = create_cli()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
