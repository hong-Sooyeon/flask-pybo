from flask import Flask, request, redirect, url_for, render_template, Blueprint
import os
from werkzeug.utils import secure_filename
from flask import Response
from werkzeug.datastructures import Headers

UPLOAD_FOLDER = 'pybo/static/images/user_img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

bp = Blueprint('test4', __name__, url_prefix='/test4')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@bp.route('/file_list/', methods=['GET', 'POST'])
def photo_list():
    return render_template('upload2.html')

@bp.route('/file_upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("upload2.html")
    return render_template("upload2_2.html")


@bp.route('/file_download')
def generate_large_csv():
    download_file = request.args.get('filename')

    full_path = os.path.join(app.config['UPLOAD_FOLDER'], download_file)

    headers = Headers()
    headers.add('Content-Disposition', 'attachment', filename=download_file)
    headers['Content-Length'] = os.path.getsize(full_path)
    download_obj = open(full_path, 'rb')

    def generate():
        for block in iter(lambda: download_obj.read(4096), b""):
            yield block
        download_obj.close()
    return Response(generate(), mimetype='application/octet-stream', headers=headers)

























# from flask import Flask, request, redirect, url_for, render_template, Blueprint
# from werkzeug.utils import redirect
# import os
# from werkzeug.utils import secure_filename
# from flask import Response
# from werkzeug.datastructures import Headers
#
# bp = Blueprint('test4', __name__, url_prefix='/test4')
# now_idx = 1
#
# @bp.route('/exercise/', methods=('GET', 'POST'))
# def uploaded():
#     return render_template('upload2.html', user_img=now_idx)
#
# @bp.route('/file_upload/', methods=['POST'])
# def upload_file():
#     global now_idx
#     uploaded_files = request.files["file"]
#     uploaded_files.save("pybo/static/images/user_img/{}.jpg".format(now_idx))
#     # print(uploaded_files)
#     now_idx += 1
#     return redirect(url_for("test4.uploaded"))
