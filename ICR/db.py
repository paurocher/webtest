import sqlite3
from datetime import datetime

import click
from flask import current_app, g

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    """

    https://flask.palletsprojects.com/en/stable/tutorial/database/#register-with-the-application

    Args:
        app:

    Returns:

    """
    # tells Flask to call that function when cleaning up after returning the
    # response.
    app.teardown_appcontext(close_db)
    # adds a new command that can be called with the flask command
    app.cli.add_command(init_db_command)


@click.command('init-db')
def init_db_command():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        script = f.read().decode('unicode_escape')
    db.cursor().executescript(script)
    db.commit()
    db.close()

    click.echo('Initialized the database.')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()