import re


def validate_email(email):
    """Validate email format using regex.

    Returns a dict with 'valid' (bool) and 'error' (str or None).
    """
    if email is None or not isinstance(email, str) or email.strip() == "":
        return {"valid": False, "error": "Email is required"}

    email_pattern = re.compile(
        r"^[a-zA-Z0-9][a-zA-Z0-9._%+-]*@[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$"
    )

    if not email_pattern.match(email):
        return {"valid": False, "error": "Invalid email format"}

    return {"valid": True, "error": None}


def validate_password(password):
    """Validate password strength.

    Returns a dict with 'valid' (bool) and 'errors' (list of strings).
    Checks: min 8 chars, at least one uppercase, one lowercase, one digit,
    one special character.
    """
    errors = []

    if password is None or not isinstance(password, str):
        return {"valid": False, "errors": ["Password is required"]}

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
    'password' keys).
    """
    email_result = validate_email(email)
    password_result = validate_password(password)

    return {
        "valid": email_result["valid"] and password_result["valid"],
        "errors": {
            "email": email_result["error"],
            "password": password_result["errors"],
        },
    }
