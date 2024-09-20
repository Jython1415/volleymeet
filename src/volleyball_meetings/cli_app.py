import argparse

def create_meeting(args):
    print(f"Creating a meeting with title: {args.title}")

def update_meeting(args):
    print(f"Updating meeting with ID: {args.id} to title: {args.title}")

def delete_meeting(args):
    print(f"Deleting meeting with ID: {args.id}")

def create_cli():
    parser = argparse.ArgumentParser(description="Basic CLI for managing meetings.")
    subparsers = parser.add_subparsers(title="Commands", help="Available commands")

    # Create Meeting Command
    create_parser = subparsers.add_parser('create', help="Create a new meeting")
    create_parser.add_argument('--title', required=True, help="Title of the meeting")
    create_parser.set_defaults(func=create_meeting)

    # Update Meeting Command
    update_parser = subparsers.add_parser('update', help="Update an existing meeting")
    update_parser.add_argument('--id', required=True, help="ID of the meeting to update")
    update_parser.add_argument('--title', required=True, help="New title of the meeting")
    update_parser.set_defaults(func=update_meeting)

    # Delete Meeting Command
    delete_parser = subparsers.add_parser('delete', help="Delete a meeting")
    delete_parser.add_argument('--id', required=True, help="ID of the meeting to delete")
    delete_parser.set_defaults(func=delete_meeting)

    return parser

if __name__ == "__main__":
    parser = create_cli()
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
