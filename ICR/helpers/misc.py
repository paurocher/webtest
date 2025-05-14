from flask import redirect, render_template, session, request
from functools import wraps
import os
from user_agents import parse
from werkzeug.user_agent import UserAgent


def login_required(f: callable) -> callable:
    """Decorate routes to require login.

    f (callable): the function to be decorated

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def new_password_quality(
    username: str,
    password: str,
    confirmation: str) -> str:
    """Makes sure the new password is strong.

    Args:
        username (str): the user name
        password (str): the old password
        confirmation (str): the new password

    Returns:
        str
    """
    error: str = ""
    # series of checks to make sure the password and username fills the
    # requirements
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    if len(password) < 6:
        error = f"Password must be at least 6 characters long."
    if password.isalnum():
        error = f"Password must contain at least one special character."
    if password != confirmation:
        error = f"Password and confirmation must match."

    return error


def validate_file_type(path: str, allowed_extensions: list) -> bool:
    """Make sure the given file is in the allowed formats."""

    # ext without the dot
    try:
        ext: str = os.path.splitext(path)[1].lower()[1:]
    except IndexError:
        return False
    if ext in allowed_extensions:
        return True
    return False

def is_mobile() -> bool:
    user_agent: str = request.headers.get("User-Agent")
    user_agent_parsed: UserAgent = parse(user_agent)
    device_type: str = (
        "Mobile" if user_agent_parsed.is_mobile else
        "Tablet" if user_agent_parsed.is_tablet else
        "Desktop"
    )
    mobile: bool = True
    if device_type == "Desktop":
        mobile = False
    return mobile