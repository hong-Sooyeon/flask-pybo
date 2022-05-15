from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required

bp = Blueprint('apply', __name__, url_prefix='/apply')

@bp.route('/apply/', methods=('GET', 'POST'))
def make():
    return render_template('apply/apply_make.html')