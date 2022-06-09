from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required

bp = Blueprint('exercise', __name__, url_prefix='/exercise')

@bp.route('/exercise/', methods=('GET', 'POST'))
def info():
    return render_template('exercise/exercise_form.html')

