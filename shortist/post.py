from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import urllib

from shortist.auth import login_required
from shortist.db import get_db

bp = Blueprint('post', __name__)

@bp.route('/', methods=('GET','POST'))
def index(destination_value=""):
    """Present form to shorten a link"""
    if request.method == 'POST':
        destination = request.form['destination']
        shortened_url = request.form['shortened']
        db = get_db()
        error = None

        if not destination:
            error = 'URL destination is required.'
        elif not shortened_url:
            error = 'Shortened URL is required.'

        if error is None:
            try:
                if not (destination.startswith("https://") or destination.startswith("http://")):
                    destination = "https://" + destination
                db.execute(
                    "INSERT INTO urls (full_url, shortened_url) VALUES (?, ?)",
                    (destination, shortened_url),
                )
                db.commit()
            except db.IntegrityError:
                error = f"This shortened URL is unavailable, choose another one."
                destination_value=destination
            else:
                return redirect(url_for('post.success', shortened=shortened_url))
        
        if error:
            flash(error)

    return render_template('post.html', destination_value=destination_value)

@bp.route('/<shortened>')
def redirect_to_destination(shortened):
    destination = get_db().execute(
        'SELECT full_url FROM urls WHERE shortened_url=?', (shortened,)
    ).fetchone()

    if not destination:
        return redirect(url_for('post.index'))

    return redirect(destination['full_url'])

@bp.route("/success/<shortened>")
def success(shortened):
    shortened_url_absolute = request.url_root + shortened
    return render_template('success.html', url=shortened_url_absolute, back=request.url_root)