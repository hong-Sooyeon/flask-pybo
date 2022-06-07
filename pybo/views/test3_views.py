from flask import Flask, request, redirect, url_for, render_template, Blueprint
import os
from werkzeug.utils import secure_filename
from flask import Response
from werkzeug.datastructures import Headers

UPLOAD_FOLDER = 'pybo/static/images/user_img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

bp = Blueprint('test3', __name__, url_prefix='/test3')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@bp.route('/file_upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return "fileupload ok"
    return render_template("upload.html")


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