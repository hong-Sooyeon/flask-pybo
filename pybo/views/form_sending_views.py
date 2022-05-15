from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required

bp = Blueprint('form_sending', __name__, url_prefix='/form_sending')

@bp.route('/form_sending/', methods=('GET', 'POST'))
def send():
    return render_template('form_sending/form_sending.html')