import os
import sys

from flask import (
    Blueprint,
    flash,
    Flask,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_session import Session

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from ICR.helpers import (
    sql_functions as sql,
)

# Configure application
app = Flask("IRC")
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



def run():
    post_data = {
        "title": "test title",
        "body": "test body",
        "images": [],
        "locations": [],
        "tags": []
    }
    sql.insert(post_data)


if __name__ == "__main__":
    run()