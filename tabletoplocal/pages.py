from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from tabletoplocal.auth import login_required
from tabletoplocal.db import get_db

bp = Blueprint('pages', __name__)

@bp.route('/')
def landing():
    return render_template('pages/landing.html')

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

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/files')
@login_required
def files():
    return render_template('pages/files.html')

@bp.route('/games', methods=('GET','POST'))
@login_required
def games():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        host = request.form['host']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tables (name, link, host)'
                ' VALUES (?, ?, ?)',
                (title, link, host)
            )
            db.commit()
            return redirect(url_for('pages.games'))

    return render_template('pages/games.html', games=get_games(), role=g.user['role'])

def get_games():
    games = get_db().execute(
        'SELECT COUNT(*) FROM tables'
    ).fetchone()[0]
    return games


@bp.route('/resources')
@login_required
def resources():
    return render_template('pages/resources.html')
