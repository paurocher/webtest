import sqlite3
from sqlite3 import Connection
from datetime import datetime

import click
from flask import Flask, current_app, g

# Tells Python how to interpret timestamp values in the database.
# We convert the value to a datetime.datetime.
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app: Flask) -> None:
    """

    https://flask.palletsprojects.com/en/stable/tutorial/database/#register-with-the-application

    Args:
        app:

    Returns:

    """
    # tells Flask to close the connection to the DB when cleaning up after
    # returning the response.
    app.teardown_appcontext(close_db)
    # adds a new command that can be called with the flask command
    app.cli.add_command(init_db_command)


@click.command('init-db')
def init_db_command() -> None:
    db: Connection = get_db()
    with current_app.open_resource("schema.sql") as f:
        script: str = f.read().decode('unicode_escape')
    db.cursor().executescript(script)
    db.commit()
    db.close()

    click.echo('Initialized the database.')


def get_db() -> Connection:
    if 'db' not in g:
        g.db: Connection = sqlite3.connect(
            current_app.config['FLASK_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e: None = None) -> None:
    """CLose the db connection.

    Args:
        e (Exception): exception instance if an error occurred.
    """
    db: Connection = g.pop('db', None)

    if db is not None:
        db.close()