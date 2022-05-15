from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required

bp = Blueprint('calculator', __name__, url_prefix='/calculator')

@bp.route('/calculator/', methods=('GET', 'POST'))
def amount():
    return render_template('calculator/calculator_amount.html')