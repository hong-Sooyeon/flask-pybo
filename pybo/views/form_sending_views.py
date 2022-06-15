import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, Blueprint, app, flash, Flask
from werkzeug.utils import secure_filename

bp = Blueprint('form_sending', __name__, url_prefix='/form_sending')
#email library

@bp.route('/sending_form/', methods=('GET', 'POST'))
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




def send_email(senders, receiver, file, title, content):
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

        # Setting
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