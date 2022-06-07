from datetime import datetime

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required
from pybo.forms import UserLoginForm




bp = Blueprint('calculator', __name__, url_prefix='/calculator')

@bp.route('/calculator/', methods=['GET', 'POST'])
def amount():
    if request.method == "POST":
        tuition_fee = float(request.form['tuition_fee'])
        result = int(tuition_fee * 0.8)
        if result <=150000:
            return render_template('calculator/calculator_amount2.html', result=result)
        if result > 150000:
            return render_template('calculator/calculator_amount2.html', result=150000)
    return render_template('calculator/calculator_amount.html')