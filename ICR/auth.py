import functools

from flask import (
    Blueprint,
    Response,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlite3 import Connection
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from ICR.helpers.misc import new_password_quality

bp = Blueprint('auth', __name__, url_prefix='/auth')


# associate the URL /register with the register view function
@bp.route('/register', methods=('GET', 'POST'))
def register() -> Response or str:
    """Register a new user.

    Returns:
        Response: rendered template
    """
    username = None
    if request.method == 'POST':
        # gather form field values
        username: str = request.form['username']
        password: str = request.form['password']
        confirmation: str = request.form.get("confirmation")

        db = get_db()

        # check password complies with requirements
        error: str = new_password_quality(username, password, confirmation)

        if not error:
            # check if username is already in the DB
            existing_name: list = db.execute(
                "SELECT name FROM users WHERE name IS ?;",
                (username, )
            ).fetchall()
            existing_name = [user['name'] for user in existing_name]
            if existing_name:
                error: str = f"User {username} is already registered."

            # all tests passed: insert new user in the DB
            try:
                db.execute(
                    "INSERT INTO users (name, hash) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Unable to create user {username}."
            else:
                return redirect(url_for("auth.login"))

        # some test failed: flash the error
        flash(error)

    return render_template('auth/register.html', username=username)


# associate the URL /login with the login view function
@bp.route('/login', methods=('GET', 'POST'))
def login() -> str or Response:
    """Log a user in.

    Returns:
        str or Response: rendered template
    """
    if request.method == 'POST':
        # gather form field values
        username: str = request.form['username']
        password: str = request.form['password']

        db: Connection = get_db()

        error: str or None = None

        # get user from the DB
        user: str = db.execute(
            'SELECT * FROM users WHERE name = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['hash'], password):
            error = 'Incorrect password.'

        if error is None:
            # empty the session
            session.clear()
            # store the user id in a new session and return to the index
            session['user_id'] = user['id']
            # set the session to permanent, but will be deleted after closing
            # the browser and the amount of seconds set to
            # PERMANENT_SESSION_LIFETIME in the config file
            session.permanent = True
            return redirect(url_for('index'))

        # some test failed: flash the error
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user() -> None:
    """Set the g.user variable.

    This function is run before each request to check if the user is logged in,
    sets the g.user variable to user or None so the pages render as a logged-in
    user or not.
    """
    user_id: int = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user: str = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


# associate the URL /logout with the logout view function
@bp.route('/logout')
def logout() -> Response:
    """Log the user out by clearing the session.

    Returns:
        Response: redirect to the index
    """
    session.clear()
    return redirect("/")


def login_required(view) -> Response:
    """Manage view based on user logged in or not.

    If the user is logged in, this returns the view passed in as an argument,
    otherwise it returns the login page.

    Returns:
        Response: rendered template
    """
    # Update a wrapper function to look like the wrapped function.
    # https://docs.python.org/3/library/functools.html#functools.wraps
    @functools.wraps(view)
    def wrapped_view(**kwargs) -> Response:
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


# associate the URL /psswd_change with the psswd_change view function
@bp.route('/psswd_change', methods=('GET', 'POST'))
def psswd_change() -> Response or str:
    """Change the password.

    Returns:
        Response: rendered template
    """
    if request.method == "POST":
        if request.form.get("action") == "Submit":
            # Get form values
            old_password: str = request.form["old_password"]
            new_password: str = request.form["new_password"]
            confirmation: str = request.form["confirmation"]

            error = False
            # checks specific to password upadte
            if not all([old_password, new_password, confirmation]):
                flash("All fields must be filled in.")
                error = True
            elif not check_password_hash(g.user["hash"], old_password):
                flash("Incorrect password.")
                error = True
            elif new_password != confirmation:
                error = True
                flash("Password and confirmation must match.")
            if error:
                return render_template("auth/psswd_change.html")

            # check password complies with requirements
            error = new_password_quality("NONE", new_password, confirmation)
            if error:
                flash(error)
                return render_template("auth/psswd_change.html")

            db = get_db()
            # update password in the DB
            db.execute(
                "UPDATE users SET hash = ? WHERE id = ?",
                (generate_password_hash(new_password), g.user["id"]),
            )
            db.commit()
            flash("Password changed.")
            return redirect(url_for('index'))

        else:
            # cancel button was pressed, go back to index
            return redirect(url_for('index'))

    elif request.method == "GET":
        return render_template("auth/psswd_change.html")

    return render_template("auth/psswd_change.html")
