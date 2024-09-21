import uuid

def create_meeting(args):
    meeting_id = str(uuid.uuid4())
    print(f"Meeting created with ID: {meeting_id}")

def update_meeting(args):
    print(f"Meeting {args.id} updated to title: {args.title}")

def delete_meeting(args):
    print(f"Meeting {args.id} deleted")