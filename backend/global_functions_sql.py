import uuid, re


def generate_uuid():
    """Generates a UUID."""
    return str(uuid.uuid4())


def is_valid_email(email):
    """Validates an email address using a regex."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_date(date):
    pass
