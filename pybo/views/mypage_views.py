from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request, g
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserLoginForm
from pybo.models import Question, Answer, User, Photo
from .auth_views import login_required
from sqlalchemy import func

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/modify/', methods=('GET', 'POST'))
def modify_info():
    current_user = g.user.id
    star = db.session.query(Photo).filter(Photo.user_id.like(current_user)).count()
    return render_template('mypage/modify_info.html', variable=star)

