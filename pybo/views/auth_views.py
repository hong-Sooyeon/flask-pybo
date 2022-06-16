from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm, UserConfirmForm, UserModifyForm    #UserConfirmForm 직원인증용. 안돌면 삭제
from pybo.models import User, UserConfirm  #UserConfirm은 직원인증위해 추가한거임. 안돌면 삭제
import functools
import time

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/confirm/', methods=('GET', 'POST'))
def confirm():
    form = UserConfirmForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = UserConfirm.query.filter_by(usernumber=form.usernumber.data).first()
        # usernumber = user.usernumber
        if not user:
            flash("직원이 아닙니다.")
        elif user.password != form.password.data:   #user.password=db에 저장된 하나포탈 비번
            flash("하나포탈 비밀번호가 올바르지 않습니다.")
        elif error is None:
            return redirect(url_for('auth.signup', usernumber=user.usernumber))   #회원가입시 행번정보 연동하여 가져감
    return render_template('auth/confirm.html', form=form)

@bp.route('/signup/<int:usernumber>', methods=('GET', 'POST'))
def signup(usernumber):
    form = UserCreateForm()
    usernumber = usernumber
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data,
                        usernumber=usernumber)   #행번정보는 confirm시 가져온 값 그대로 가져감
            db.session.add(user)
            db.session.commit()
            flash('가입을 환영합니다.')
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', usernumber=usernumber, form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view

#비밀번호 잊었을때 행번,포탈비번으로 인증후 재설정하는거
@bp.route('/reset/', methods=('GET', 'POST'))
def reset_pw1():
    form = UserConfirmForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = UserConfirm.query.filter_by(usernumber=form.usernumber.data).first()
        if not user:
            flash("직원이 아닙니다.")
        elif user.password != form.password.data:   #user.password=db에 저장된 하나포탈 비번/
            flash("하나포탈 비밀번호가 올바르지 않습니다.")  #form.password.data는 user가 input하는 비번
        elif error is None:
            return redirect(url_for('auth.reset_pw2', usernumber=user.usernumber))
    return render_template('auth/confirm.html', form=form)

@bp.route('/reset_pw/<int:usernumber>', methods=('GET', 'POST'))
def reset_pw2(usernumber):
    form = UserModifyForm()
    user = db.session.query(User).filter_by(usernumber=usernumber).first()
    if request.method == 'POST' and form.validate_on_submit():
        new_password = generate_password_hash(form.password1.data)
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        flash("비밀번호가 재설정 되었습니다")
    return render_template('auth/reset_pw.html', form=form)
