<<<<<<< HEAD
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
=======
# # email library
# import os
# import smtplib
# from email import encoders
# from email.header import Header
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
from flask import request, render_template, Blueprint, app, flash, Flask
from pybo.views.auth_views import login_required
#
# # import sys
# # from PyQt5.QtCore import *
# # from PyQt5.QtGui import *
# # from PyQt5.QtWebKit import *
# #
# # app = QApplication(sys.argv)
# # w = QWebView()
# # w.load(QUrl('https://www.delftstack.com'))
# # p = Qp()
# # p.setPageSize(Qp.A4)
# # p.setOutputFormat(Qp.PdfFormat)
# # p.setOutputFileName("sample.pdf")
# #
# # def convertIt():
# #     w.print_(p)
# #     QApplication.exit()
# #
# # QObject.connect(w, SIGNAL("loadFinished(bool)"), convertIt)
# # sys.exit(app.exec_())f


# from flask import Blueprint, url_for, render_template, flash, request
# from werkzeug.utils import redirect
#
# from pybo import db
# from ..forms import AnswerForm
# from pybo.models import Question, Answer
# from .auth_views import login_required
>>>>>>> 817cd5959d0d6dfce9ba967420741d5d3a4bbbdf

from flask import request, render_template, Blueprint, app, flash, Flask
from werkzeug.utils import secure_filename

bp = Blueprint('form_sending', __name__, url_prefix='/form_sending')
#email library

<<<<<<< HEAD
@bp.route('/sending_form/', methods=('GET', 'POST'))
=======
@bp.route('/form_sending', methods=('GET', 'POST'))
@login_required
>>>>>>> 817cd5959d0d6dfce9ba967420741d5d3a4bbbdf
def email_test():
    if request.method == 'POST':
        senders = 'hanabankhconnect@gmail.com'
        receiver = request.form["email_receiver"]

        file = request.files["email_file"]
        title = request.form["email_title"]
        content = request.form["email_content"]

        result = send_email(senders, receiver, file, title, content)

        if not result:
            return render_template('form_sending/form_sending.html', content="Email is sent")
        else:
            return render_template('form_sending/form_sending.html', content="Email is not sent")

    else:
        return render_template('form_sending/form_sending.html')




<<<<<<< HEAD
def send_email(senders, receiver, file, title, content):
=======
@bp.route('/send_email', methods=('GET', 'POST'))
@login_required
def send_email(receiver, file, title, content):
>>>>>>> 817cd5959d0d6dfce9ba967420741d5d3a4bbbdf
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = senders
        msg['To'] = receiver
        msg['Subject'] = Header(title, 'euc-kr')  # 제목 인코딩
        msg.attach(MIMEText(content, 'plain', 'euc-kr'))  # 내용 인코딩
        #msg.attach(MIMEText(html, 'html', 'euc-kr'))  # 내용 인코딩 2


        # 아래 코드는 첨부파일이 있을 경우에만 주석처리 빼시면 됩니다.
        # 첨부 파일 보내기
        file.save(secure_filename(file.filename))
        filename = file.filename  # 첨부 파일 이름 이처럼 이름만쓰려면 같은 경로에 파일있어야됨 아니면 절대경로입력
        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(part)

        # Server config
        MAIL_SERVER = 'smtp.gmail.com'
        MAIL_PORT = 587
        MAIL_USERNAME = 'hanabankhconnect@gmail.com'
        # 'rlaqks2@gmail.com'
        APP_PASSWORD = 'lraytzluklrnmtgn'
        # 'mxkdwcprhhxhrqpu'

        # Settingg
        mailServer = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(MAIL_USERNAME, APP_PASSWORD)
        mailServer.sendmail(senders, receiver, msg.as_string())
        mailServer.close()

    except Exception as e:
        print(e)
        pass
    finally:
        print('success')
        pass