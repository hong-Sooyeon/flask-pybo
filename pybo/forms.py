from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=2, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    # 회원가입시 행번정보 받기위해 만든거. 안되면 삭제
    usernumber = IntegerField('행번')

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호확인', validators=[DataRequired()])


#위에까지가 original------------------------------------------------------------------------------

#직원 검증 위해 새로 만드는거
class UserConfirmForm(FlaskForm):
    usernumber = IntegerField('행번', validators=[DataRequired()])
    password = PasswordField('하나포탈비밀번호', validators=[DataRequired()])

class PhotoForm(FlaskForm):
    # content = StringField('사진', validators=[DataRequired('사진은 필수입력 항목입니다.')])
    content = StringField('사진')

class UserModifyForm(FlaskForm):
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])