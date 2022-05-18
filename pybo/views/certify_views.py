from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required

bp = Blueprint('certify', __name__, url_prefix='/certify')

@bp.route('/exercise/', methods=('GET', 'POST'))
def certification():
    return render_template('certify/certification.html')

