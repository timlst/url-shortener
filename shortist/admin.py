from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from shortist.auth import login_required
from shortist.db import get_db

"""
The admin page that allows viewing all registered links.
"""

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@login_required
def overview():
    """Display all registered links"""
    db = get_db()
    links = db.execute(
        'SELECT id, shortened_url, full_url, created FROM urls ORDER BY created ASC'
    ).fetchall()
    return render_template('admin/index.html', links=links)

@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
    """Deletes url with id from database"""
    db = get_db()
    db.execute(
        'DELETE FROM urls WHERE id=?', (id,) 
    )
    db.commit()
    return redirect(url_for('admin.overview'))
