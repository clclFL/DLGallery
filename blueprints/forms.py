from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, ValidationError
from werkzeug.security import check_password_hash  # 解密

from models import User
from exts import r


class LoginForm(FlaskForm):
    username = StringField(label=u"Username", validators=[
        DataRequired(),
        Length(min=3, max=10)
    ])
    password = PasswordField(label=u"Password", validators=[
        DataRequired(message="password cannot be empty"),
        Length(min=6)
    ])
    submit = SubmitField(label=u"Login")

    def validate_username(self, username_field):
        if not User.query.filter_by(username=username_field.data).first():  # 用户名不存在
            raise ValidationError('Username not exist')


class RegisterForm(LoginForm):
    email = EmailField(label=u"Email Address", validators=[
        DataRequired(),
    ])
    captcha = StringField(label=u"Captcha", validators=[
        DataRequired(),
        Length(min=6, max=6)
    ])
    submit = SubmitField(label=u"Register")

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():  # 邮箱已经存在
            raise ValidationError('Email already registered')

    def validate_captcha(self, captcha_field):
        captcha = r.get(self.email.data)
        if not captcha:
            raise ValidationError('No captcha has been sent')
        if captcha != captcha_field.data:
            raise ValidationError('Captcha does not match')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():  # 用户名已经存在
            raise ValidationError('Username already registered')

