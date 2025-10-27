# INF601 - Advanced Programming in Python

# Kody Kirk

# Mini Project 3

# This project will be using Flask to deploy a small web app of your choice. The goal here is to come up with a small web application that meets the requirements below. If you get stuck here, please email me!
#
#     (5/5 points) Initial comments with your name, class and project at the top of your .py file.
#     (5/5 points) Proper import of packages used.
#     (70/70 points) Using Flask you need to setup the following:
#     (10/10 points) Setup a proper folder structure, use the tutorial as an example.
#     (20/20 points) You need to have a minimum of 5 pages, using a proper template structure.
#     (10/10 points) You need to have at least one page that utilizes a form and has the proper GET and POST routes setup.
#     (10/10 points) You need to setup a SQLlite database with a minimum of two tables, linked with a foreign key.
#     (10/10) You need to use Bootstrap in your web templates. I won't dictate exactly what modules you need to use but the more practice here the better. You need to at least make use of a modal.
#     (10/10) You need to setup some sort of register and login system, you can use the tutorial as an example.
#     (5/5 points) There should be a minimum of 5 commits on your project, be sure to commit often!
#     (5/5 points) I will be checking out the main branch of your project. Please be sure to include a requirements.txt file which contains all the packages that need installed. You can create this fille with the output of pip freeze at the terminal prompt.
#     (10/10 points) There should be a README.md file in your project that explains what your project is, how to install the pip requirements, and how to execute the program. Please use the GitHub flavor of Markdown. Be thorough on the explanations. You will need to explain the steps of initializing the database and then how to run the development server for your project.

import sqlite3
from datetime import datetime

import click
from flask import current_app, g


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
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
