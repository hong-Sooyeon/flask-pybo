from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm, UserConfirmForm    #UserConfirmForm 직원인증용. 안돌면 삭제
from pybo.models import User, UserConfirm  #UserConfirm은 직원인증위해 추가한거임. 안돌면 삭제
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

#계정생성 첫단계, 행번과 포탈 비번으로 직원인증하는 화면 추가함(파이보 수업에 추가1)
@bp.route('/confirm/', methods=('GET', 'POST'))
def confirm():
    form = UserConfirmForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = UserConfirm.query.filter_by(usernumber=form.usernumber.data).first()
        if not user:
            flash("직원이 아닙니다.")
        #elif not check_password_hash(user.password, form.password.data):
        # 로그인함수에서는 위의 코드로 비번 이걸로 확인했음. 여기서는 작동안됨
        elif user.password != form.password.data:   #user.password=db에 저장된 하나포탈 비번/
            flash("하나포탈 비밀번호가 올바르지 않습니다.")  #form.password.data는 user가 input하는 비번
        elif error is None:
            return redirect(url_for('auth.signup'))
    return render_template('auth/confirm.html', form=form)

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

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