from flask import redirect, session, request
from functools import wraps
import os
from user_agents import parse
from werkzeug.user_agent import UserAgent


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
        error = "Password must be at least 6 characters long."
    if password.isalnum():
        error = "Password must contain at least one special character."
    if password != confirmation:
        error = "Password and confirmation must match."

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
    """Determine if the current request is from a mobile device.

    Analyzes the 'User-Agent' header from the request to deduce the type of
    device making the request. Returns True if the device is a mobile or
    tablet, and False if it's a desktop.

    Returns:
        bool: True if the device is mobile or tablet, False if desktop.
    """
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
