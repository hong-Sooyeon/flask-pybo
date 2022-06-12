from flask import Flask, Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect
from flask_mail import Mail, Message
from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required

bp = Blueprint('apply', __name__, url_prefix='/apply')

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.naver.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'k2hmal@naver.com'
app.config['MAIL_PASSWORD'] = 'tkfkdgPrud1121@'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



@bp.route('/apply/', methods=('GET', 'POST'))
def make():
    if request.method == 'POST':
        senders = 'k2hmal@naver.com'
        receiver = 'k2hmal2@gmail.com'
        content = 'document'


        result = send_email(senders, receiver, content)

        if not result:
            return render_template('email.html', content="Email is sent")
        else:
            return render_template('email.html', content="Email is not sent")

    else:
        return render_template('apply/apply_make.html')


def send_email(senders, receiver, content):
    try:
        mail = Mail(app)
        msg = Message('Title', sender=senders, recipients=receiver)
        msg.body = content
        mail.send(msg)
    except Exception:
        pass
    finally:
        pass