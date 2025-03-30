from flask import redirect, render_template, session, request
from functools import wraps
import os
from user_agents import parse
from werkzeug.user_agent import UserAgent


# from ICR.__app import app


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

def validate_file_type(path, allowed_extensions):
    """Make sure the given file is in the allowed formats."""

    # ext without the dot
    try:
        ext = os.path.splitext(path)[1].lower()[1:]
    except IndexError:
        return False
    if ext in allowed_extensions:
        return True
    return False

def is_mobile():
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