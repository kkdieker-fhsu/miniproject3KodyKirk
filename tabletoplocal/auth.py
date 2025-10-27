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

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from tabletoplocal.db import get_db

import random

bp = Blueprint('auth', __name__, url_prefix='/auth')

def newclr():
    return f"#{random.randint(0, 0xFFFFFF):06x}"

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, color) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), newclr()),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('landing'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

