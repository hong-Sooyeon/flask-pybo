from flask import Flask, Blueprint, render_template


from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer, User
from .auth_views import login_required


bp = Blueprint('/hongtest/', __name__, url_prefix='/hongtest/')

@bp.route('/hongtest/', methods=('GET', 'POST'))

def hongtest():
    User.username = User.query.get_or_404(User.username)
    return render_template('form_sending/hongtest.html', user=User.username, data={'level':60,'point':360,'exp':45000})