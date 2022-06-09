from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from .. import db
from ..models import Question, Answer, User
from ..forms import QuestionForm, AnswerForm
from pybo.views.auth_views import login_required

bp = Blueprint('hconnect', __name__, url_prefix='/hconnect')

@bp.route('/hconnect/', methods=('GET', 'POST'))
def screen():
    return render_template('hconnect/screen_main2.html')
