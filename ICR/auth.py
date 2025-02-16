import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    username = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmation = request.form.get("confirmation")
        db = get_db()

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'


        if password != confirmation:
            error = f"Password and confirmation must match."

        if not error:
            existing_name = db.execute(
                "SELECT name FROM users WHERE name IS ?;",
                (username)
            ).fetchall()
            existing_name = [user['name'] for user in existing_name]
            if existing_name:
                error = f"User {username} is already registered."

        if error is None:
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

        flash(error)

    return render_template('auth/register.html', username=username)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE name = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['hash'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect("/")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
