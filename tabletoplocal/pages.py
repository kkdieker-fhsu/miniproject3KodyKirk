import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import send_from_directory

from tabletoplocal.auth import login_required
from tabletoplocal.db import get_db

bp = Blueprint('pages', __name__)

#the landing page
@bp.route('/')
def landing():
    return render_template('pages/landing.html')

#the chat page and associated function to get chat messages from database
@bp.route('/chat', methods=('GET', 'POST'))
@login_required
def chat():
    db = get_db()
    chats = db.execute(
        'SELECT p.id, body, created, author_id, username, color'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created ASC'
        ' LIMIT 100'
    ).fetchall()
    return render_template('pages/chat.html', chats=chats)

#add new chat message to the database
@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        body = request.form['body']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (body, author_id)'
                ' VALUES (?, ?)',
                (body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('pages.chat'))

    return redirect(url_for('pages.chat'))

#the files page and its functions
@bp.route('/files')
@login_required
def files():
    if not os.path.exists('uploads'):
        os.mkdir('uploads')
    upload_path = 'uploads'
    filetree = filetree(upload_path)

    return render_template('pages/files.html', filetree=filetree)

def filetree(fullpath):
    tree = []
    for root, dirs, files in os.walk(fullpath):
        for name in sorted(files):
            path = os.path.join(root, name)
            tree.append(path)
    return tree

@bp.route('/uploads/<path:filename>')
@login_required
def download(filename):
    folder = 'uploads'
    try:
        return send_from_directory(folder, filename)

    except FileNotFoundError:
        abort(404)

#the games page and associated functions
@bp.route('/games', methods=('GET','POST'))
@login_required
#add new game data to the database
def games():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        host = request.form['host']
        system = request.form['system']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tables (name, link, host, system)'
                ' VALUES (?, ?, ?, ?)',
                (title, link, host, system)
            )
            db.commit()
            return redirect(url_for('pages.games'))

    return render_template('pages/games.html', games=get_games(), role=g.user['role'], servers=active_servers())

#get the number of games in the database
def get_games():
    games = get_db().execute(
        'SELECT COUNT(*) FROM tables'
    ).fetchone()[0]
    return games

#get data on the active servers
def active_servers():
    servers = get_db().execute(
        'SELECT * FROM tables'
    ).fetchall()
    return servers

#load the resources page
@bp.route('/resources')
@login_required
def resources():
    return render_template('pages/resources.html')

