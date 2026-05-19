import re

# Module-level compiled regex for email validation (compiled once, reused)
_EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+\-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$"
)

# Maximum lengths
_MAX_EMAIL_LENGTH = 254  # RFC 5321
_MAX_PASSWORD_LENGTH = 128


def validate_email(email):
    """Validate email format using regex.

    Returns a dict with 'valid' (bool) and 'errors' (list of strings).

    Raises:
        ValueError: If email is None, not a string, or whitespace-only.
    """
    if email is None or not isinstance(email, str):
        raise ValueError("Email is required")

    if email.strip() == "":
        raise ValueError("Email is required")

    if len(email) > _MAX_EMAIL_LENGTH:
        return {"valid": False, "errors": ["Email must not exceed 254 characters"]}

    if not _EMAIL_PATTERN.match(email):
        return {"valid": False, "errors": ["Invalid email format"]}

    return {"valid": True, "errors": []}


def validate_password(password):
    """Validate password strength.

    Returns a dict with 'valid' (bool) and 'errors' (list of strings).
    Checks: min 8 chars, max 128 chars, at least one uppercase, one lowercase,
    one digit, one special character.

    Raises:
        ValueError: If password is None, not a string, or whitespace-only.
    """
    errors = []

    if password is None or not isinstance(password, str):
        raise ValueError("Password is required")

    if password.strip() == "":
        raise ValueError("Password is required")

    if len(password) > _MAX_PASSWORD_LENGTH:
        errors.append("Password must not exceed 128 characters")

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")

    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")

    if not re.search(r"[0-9]", password):
        errors.append("Password must contain at least one digit")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>\-_=+\[\]\\;'/`~]", password):
        errors.append("Password must contain at least one special character")

    return {"valid": len(errors) == 0, "errors": errors}


def validate_login_form(email, password):
    """Combine email and password validations.

    Returns a dict with 'valid' (bool) and 'errors' (dict with 'email' and
    'password' keys, both lists of strings).

    Raises:
        ValueError: Propagates ValueError from validate_email or
            validate_password if inputs are None, non-string, or whitespace-only.
    """
    email_result = validate_email(email)
    password_result = validate_password(password)

    return {
        "valid": email_result["valid"] and password_result["valid"],
        "errors": {
            "email": email_result["errors"],
            "password": password_result["errors"],
        },
    }
