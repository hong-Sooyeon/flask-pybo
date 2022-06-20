import smtplib
import datetime
from flask import Blueprint, render_template, request, g
from werkzeug.utils import secure_filename
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from pybo.views.auth_views import login_required

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('apply', __name__, url_prefix='/apply')

gmail_account_id = "hanabankhconnect@gmail.com"  # Gmail계정ID
gmail_account_pass = "lraytzluklrnmtgn"  # Gmail계정의앱비밀번호16자리

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def set_file(file):
    if file.filename == '':
        print("파일이 없습니다.")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(filename)
        return filename

def makeHtml(filename, request):
    html_text = '''
        <!doctype html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport"
                      content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>신청확인서</title>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Do+Hyeon&display=swap');
                </style>
            </head>
            <body>
                <div style="font-family: 'Do Hyeon', sans-serif;">
                    <h1 style="font-size:40px;
                        padding:20px;
                        margin-bottom: 0;
                        text-align: center;"
                    >
                        신청확인서
                    </h1>
                    <table boder = "cellspacing = 1"
                        style="margin:0 auto;
                        border-collapse: separate;
                        border-spacing: 0 3px;
                        width:300px;
                    ">
                        <tr>
                            <td class="title" style="padding: 10px 0px;font-size:18px;">■ 인적사항</td>
                        </tr>
                        <tr>
                            <td>행번</td>
                            <td>
                                {usernumber}
                            </td>
                        </tr>
                        <tr>
                            <td>성명</td>
                            <td>
                                {name}
                            </td>
                        </tr>
                        <tr>
                            <td>부점명</td>
                            <td>
                                {dept}
                            </td>
                        </tr>
                        <tr>
                            <td>직급</td>
                            <td>
                                {position}
                            </td>
                        </tr>
                        <tr>
                            <td class="title" style="padding: 10px 0px;font-size:18px;">■ 수강상세내역</td>
                        </tr>
                        <tr>
                            <td>수강과목</td>
                            <td>
                                {course}
                            </td>
                        </tr>
                        <tr>
                           <td>수강기간</td>
                           <td>
                              {course_start_time} ~ {course_end_time}
                           </td>
                        </tr>
                        <tr>
                            <td>기관명</td>
                            <td>
                                {organization_name}
                            </td>
                        </tr>
                        <tr>
                            <td>기관 전화번호</td>
                            <td>
                                {organization_tel}
                            </td>
                        </tr>
                        <tr>
                            <td>총결제금액</td>
                            <td>
                                {total_price}
                            </td>
                        </tr>
                        <tr>
                            <td>수강개월</td>
                            <td>
                                {course_month} 개월
                            </td>
                        </tr>
                        <tr>
                            <td>영수증 결제일</td>
                            <td>
                                {payment_date}
                            </td>
                        </tr>
                        <tr>
                            <td>승인번호</td>
                            <td>
                                {approval_number}
                            </td>
                        </tr>
                        <tr>
                            <td>결제카드번호</td>
                            <td>
                                {card_number}
                            </td>
                        </tr>
                    </table>
                </div>
    '''.format(
            usernumber=request.form["usernumber"],
            name=request.form["name"],
            dept=request.form["dept"],
            position=request.form["position"],
            course=request.form["course"],
            course_start_time=request.form["course_start_time"],
            course_end_time=request.form["course_end_time"],
            organization_name=request.form["organization_name"],
            organization_tel=request.form["organization_tel"],
            total_price=request.form["total_price"],
            course_month=request.form["course_month"],
            payment_date=request.form["payment_date"],
            approval_number=request.form["approval_number"],
            card_number=request.form["card_number"],
        )

    with open(filename, 'w', encoding="utf-8") as html_file:
        html_file.write(html_text)


@bp.route('/apply', methods=('GET', 'POST'))
@login_required
def make():
    info = {}

    info["name"] = g.user.name
    info["usernumber"] = g.user.usernumber
    info["dept"] = g.user.dept
    info["position"] = g.user.position

    #info["name"] = "김준희test"
    #info["usernumber"] = "1011542test"
    #info["dept"] = "인사섹션test"
    #info["position"] = "대리test"

    info["course_start_time"] = datetime.datetime.now().strftime('%Y-%m-%d')
    info["course_end_time"] = (datetime.datetime.now() + datetime.timedelta(weeks=4)).strftime('%Y-%m-%d')
    info["payment_date"] = datetime.datetime.now().strftime('%Y-%m-%d')
    files = {}
    if request.method == 'POST':

        files["email_html"] = "email.html"

        to_mail = "k2hmal@naver.com"
        from_mail = "hanabankhconnect@gmail.com"
        subject = "체력단련비 신청서"

        makeHtml(files["email_html"], request)

        files["email_file1"] = set_file(request.files['email_file1'])
        files["email_file2"] = set_file(request.files['email_file2'])
        files["email_file3"] = set_file(request.files['email_file3'])

        result = sendMultiMessage(to_mail, from_mail, subject, files)

        return render_template('apply/apply_make.html', info=request.form, files=files, result=result)
    else:
        return render_template('apply/apply_make.html', info=info, files=files)

def sendMultiMessage(to_email, from_email, subject, files):
    try:
        message = """
                    <html>
                    <body>
                        <h2>체력단련비 신청서</h2>
                        <p>작성하신 신청내역서 입니다.</p>
                    </body>
                    </html>
                """

        print("【Message와File의Email송신시작】：" + str(datetime.datetime.now()))

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["To"] = to_email
        msg["From"] = from_email
        msg.attach(MIMEText(message, 'html'))

        for path in files:
            part = MIMEBase('application', "octet-stream")
            if(files[path]):
                with open(files[path], 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename={}'.format(files[path]))
                msg.attach(part)

        # 메일송신처리
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_account_id, gmail_account_pass)
        server.send_message(msg)
        server.quit()

    except Exception as e:
        errordate = str(datetime.datetime.now())

        print("【=== 에러내용 ===】：" + errordate)
        print("type:" + str(type(e)))
        print("args:" + str(e.args))
        print("e자신:" + str(e))
        return False

    else:
        print("【정상적으로 Message와File의Email송신이 완료됬습니다.】：" + str(datetime.datetime.now()))
        return True
    finally:
        print("【Message와File의Email송신완료】：" + str(datetime.datetime.now()))
        return True

