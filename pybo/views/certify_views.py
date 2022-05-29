from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import User
from .auth_views import login_required

bp = Blueprint('certify', __name__, url_prefix='/certify')

@bp.route('/exercise/', methods=('GET', 'POST'))
def certification():
    return render_template('certify/certification.html')


# 아래부터가 새로운 코드(이미지업로드 게시판 만들기)
@bp.route('/create/', methods=('GET', 'POST'))
# @login_required
def create():
    return render_template('certify/photo_create.html')


