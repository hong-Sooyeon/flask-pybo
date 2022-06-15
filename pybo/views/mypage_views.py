from datetime import datetime
from flask import Blueprint, url_for, render_template, flash, request, g, session
from werkzeug.utils import redirect
from pybo import db
from pybo.models import Question, Answer, User, Photo
from pybo.forms import UserModifyForm
from werkzeug.security import generate_password_hash, check_password_hash
from pybo.views.auth_views import login_required

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/modify/', methods=('GET', 'POST'))
@login_required
def modify_info():
    user = g.user
    form = UserModifyForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_password = generate_password_hash(form.password1.data)
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        flash("비밀번호가 변경되었습니다")   #새로운 비밀번호 db저장
    user_name = user.username           #아래 3줄은 사용자 정보 text 표시
    user_email = user.email
    user_number = user.usernumber
    current_user = user.id
    star = db.session.query(Photo).filter(Photo.user_id.like(current_user)).count()     #photo db에서 사용자 id 횟수 count
    return render_template('mypage/modify_info.html', variable=star, username=user_name, useremail=user_email, usernumber=user_number, form=form)
