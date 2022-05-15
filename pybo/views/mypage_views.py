from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/hconnect/', methods=('GET', 'POST'))
def modify_info():
    return render_template('mypage/modify_info.html')