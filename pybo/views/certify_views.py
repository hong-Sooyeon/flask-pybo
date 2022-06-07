import base64
from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import User
from .auth_views import login_required

bp = Blueprint('certify', __name__, url_prefix='/certify')

UPLOAD_FOLDER = '/pybo/static/images/user_img'


@bp.route('/exercise/', methods=('GET', 'POST'))
def certification():
    return render_template('certify/certification.html')


# 아래부터가 새로운 코드(이미지업로드 게시판 만들기)
@bp.route('/create/', methods=('GET', 'POST'))
# @login_required
def create():
    location = request.args.get("location")
    cleaness = request.args.get("clean")
    built_in = request.args.get("built")
    if cleaness == None:
        cleaness = False
    else:
        cleaness = True
    return render_template('certify/photo_form.html')

@bp.route('/upload_done/', methods=['POST'])
# @login_required
def upload_done():
    uploaded_files = request.files["file"]
    uploaded_files.save("pybo/static/images/user_img/{}.jpg".format(22))
    return redirect(url_for("certify.certification"))



# global now_idx
# now_idx = 1
#
# def upload_done():
#
#     uploaded_files = request.files["file"]
#     uploaded_files.save("pybo/static/images/user_img/{}.jpg".format(now_idx))
#     print(uploaded_files)
#     now_idx += 1
#     return redirect(url_for("certify.certification"))





#아래꺼로하면 파일명대로 폴더에 저장은 됨. 불려지진 않음
#
# @bp.route('/upload_done/', methods=['POST'])
# # @login_required
# def upload_done():
#     file = request.files["file"]
#     filename = secure_filename(file.filename)
#     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     # uploaded_files.save("pybo/static/images/user_img/{}.jpg".format(2))
#     return redirect(url_for("certify.certification"))
