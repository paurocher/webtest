from datetime import datetime
import os

# from cs50 import SQL
from flask import (
    current_app,
    g,
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session
)
from flask_session import Session
from flask_mobility import Mobility
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

from ICR.helpers.misc import apology

# Configure application
app = Flask("IRC")

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Extra configurations
app.config.from_pyfile("ICR/config.py")
print(app.config)


DB = sqlite3.connect("ice_climbing.db", check_same_thread=False)
DB.row_factory = sqlite3.Row
cursor = DB.cursor()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/full_screen_carousel")
def full_screen_carousel():
    print("aaaaaaaaaaa")
    return render_template("full_screen_carousel.html")


# @login_required
@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pass
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = cursor.execute(
            "SELECT * FROM users WHERE name = ?",
            (request.form.get("username"),)
        )
        rows = rows.fetchone()
        print(rows)
        print(rows["name"])
        print(rows["hash"])
        print(request.form.get("password"))
        print(check_password_hash(
            rows["hash"], request.form.get("password")))

        # Ensure username exists and password is correct
        if not check_password_hash(
            rows["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        user_name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        print(user_name, password, confirmation)

        if user_name == "" or password == "" or confirmation == "":
            return apology(f"Must choose a user name.", 000)

        # verify password check
        if password != confirmation:
            return apology(f"Password and confirmation must match.", 000)

        # verify DB for for existing user
        print(DB.execute("SELECT * FROM users WHERE name IS ?",
            user_name).fetchone())
        if DB.execute("SELECT * FROM users WHERE name IS ?", user_name):
            return apology(f"User name {user_name} already exists.", 000)
        else:
            password_hash = generate_password_hash(password)
            DB.execute("INSERT INTO users (name, hash) VALUES (?, ?)", user_name, password_hash)
            # pass a flash message here
            flash('You were successfully registered!!\n  You may log in now :)')
            return render_template("login.html")
    else:
        return render_template("register.html")