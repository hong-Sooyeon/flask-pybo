from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required

bp = Blueprint('complete', __name__, url_prefix='/complete')

@bp.route('/complete/', methods=('GET', 'POST'))
def apply():
    return render_template('complete/complete_apply.html')