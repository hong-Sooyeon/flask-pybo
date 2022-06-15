
from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

# original
# @bp.route('/')
# def index():
#     return redirect(url_for('question._list'))

@bp.route('/')
def index():
    return redirect(url_for('hconnect.screen'))
#
# @bp.route('/form_sending')
# def email():
#      return redirect(url_for('form_sending.email_test'))

