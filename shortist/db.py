import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

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

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('register-user')
@click.argument("username")
@click.argument("password")
@with_appcontext
def register_user(username, password):
    db = get_db()
    try:
        db.execute(
            'INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(password))
        )
        db.commit()
    except db.IntegrityError:
        click.echo(f"User {username} already exists.", err=True)
    except db.Error as e:
        click.echo(f"Could not register user: {e}")
    else:
        click.echo(f"User {username} added to database.")

@click.command("clear-users")
@with_appcontext
def clear_users():
    db = get_db()
    try:
        db.execute(
            'DELETE FROM user;'
        )
        db.commit()
    except db.Error as e:
        click.echo(f"Could not clear users: {e}")
    else:
        click.echo(f"Users database has been cleared.")

@click.command("clear-urls")
@with_appcontext
def clear_urls():
    db = get_db()
    try:
        db.execute(
            'DELETE FROM urls;'
        )
        db.commit()
    except db.Error as e:
        click.echo(f"Could not clear urls: {e}")
    else:
        click.echo(f"URLs database has been cleared.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(register_user)
    app.cli.add_command(clear_users)
    app.cli.add_command(clear_urls)