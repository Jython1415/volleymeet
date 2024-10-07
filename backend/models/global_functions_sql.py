import uuid, re
from datetime import datetime
from dateutil import parser


def generate_uuid():
    """Generates a UUID."""
    return str(uuid.uuid4())


def is_valid_email(email):
    """Validates an email address using a regex."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def is_valid_date(date_str):
    """
    Validates and parses date strings in various human-readable formats.
    Returns True if the date can be parsed and formats the output in 'YYYY-MM-DD HH:MM AM/PM'.

    Args:
    date_str (str): The date string to validate.

    Returns:
    tuple: (bool, str or None) True if valid and formatted date string, otherwise False and None.
    """
    formats = [
        "%Y-%m-%d %I:%M %p",  # Recommended format: 'YYYY-MM-DD HH:MM AM/PM'
    ]

    for date_format in formats:
        try:
            parsed_date = datetime.strptime(date_str, date_format)
            # Return the date in the recommended 'YYYY-MM-DD HH:MM AM/PM' format
            formatted_date = parsed_date.strftime("%Y-%m-%d %I:%M %p")
            return True, formatted_date
        except ValueError:
            continue
    return False, None


if __name__ == "__main__":
    is_valid, formatted_date = is_valid_date("asdf;lkj")
    if is_valid:
        print("Valid date:", formatted_date)
    else:
        print("Invalid date")
