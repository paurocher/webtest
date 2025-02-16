import sqlite3
from datetime import datetime
import os

import click
from flask import current_app, g

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# def init_db():
#     print("pam")
#     db = get_db()
#
#     with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))
#         print("pum!")


@click.command('init-db')
def init_db_command():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        script = f.read().decode('unicode_escape')
    # print("fffffffffff", script)
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