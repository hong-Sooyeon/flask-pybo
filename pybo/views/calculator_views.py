from datetime import datetime, time

from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required
from pybo.forms import UserLoginForm




bp = Blueprint('calculator', __name__, url_prefix='/calculator')

@bp.route('/calculator/', methods=['GET', 'POST'])
@login_required
def amount():
    if request.method == "POST":
        tuition_fee = float(request.form['tuition_fee'])
        start_date = (request.form['start_date'])
        end_date = (request.form['end_date'])

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        diff = end - start
        diff_days = diff.days   #날짜 차이 구한거에서 day만 가져옴

        difference = diff_days // 30

        result = int(tuition_fee * 0.8)

        if result <= 150000:
            if difference > 0:
                amount = result * difference
                return render_template('calculator/calculator_amount2.html', result=result, period=difference, amount=amount)
            else:
                return render_template('calculator/calculator_amount2.html', result=0, period=0, amount=0)
        if result > 150000:
            if difference > 0:
                amount = 150000 * difference
                return render_template('calculator/calculator_amount2.html', result=150000, period=difference, amount=amount)
            else:
                return render_template('calculator/calculator_amount2.html', result=0, period=0, amount=0)
    return render_template('calculator/calculator_amount.html')