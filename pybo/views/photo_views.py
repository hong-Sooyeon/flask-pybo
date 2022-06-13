from datetime import datetime
import os
from flask import Flask, Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect, secure_filename

from .. import db
from ..models import Question, Answer, User, Photo
from ..forms import PhotoForm
from pybo.views.auth_views import login_required

UPLOAD_FOLDER = 'pybo/static/images/user_img'

bp = Blueprint('photo', __name__, url_prefix='/photo')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@bp.route('/photo_list/')
@login_required
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    photo_list = Photo.query.order_by(Photo.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Photo.user_id, Photo.content, User.username) \
            .join(User, Photo.user_id == User.id).subquery()
        photo_list = photo_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.user_id == User.id) \
            .filter(Photo.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    photo_list = photo_list.paginate(page, per_page=10)
    return render_template('photo/photo_list.html', photo_list=photo_list, page=page, kw=kw)

@bp.route('/photo_detail/<int:photo_id>/')
def detail(photo_id):
    form = PhotoForm()
    photo = Photo.query.get_or_404(photo_id)
    return render_template('photo/photo_detail.html', photo=photo, form=form)

@bp.route('/photo_create/', methods=('GET', 'POST'))
@login_required
def create():
    form = PhotoForm()
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo = Photo(content="/static/images/user_img/{}".format(filename), create_date=datetime.now(), user=g.user)
        db.session.add(photo)
        db.session.commit()
        return redirect(url_for('photo._list'))
    return render_template('photo/photo_form.html', form=form)

@bp.route('/photo_delete/<int:user_id>')
@login_required
def delete(user_id):
    photo = Photo.query.get_or_404(user_id)
    if g.user != photo.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('photo._list'))
    db.session.delete(photo)
    db.session.commit()
    flash('삭제가 완료되었습니다')
    return redirect(url_for('photo._list'))

