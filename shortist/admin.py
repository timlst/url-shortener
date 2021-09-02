from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from shortist.auth import login_required
from shortist.db import get_db

bp = Blueprint('blog', __name__)
