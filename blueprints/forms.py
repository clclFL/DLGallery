from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, EmailField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from werkzeug.security import check_password_hash  # 解密

from models import User, Admin
from exts import r

username_validators = [DataRequired(), Length(min=3, max=10)]
password_validators = [DataRequired(message="password cannot be empty"), Length(min=6)]
email_validators = [DataRequired()]
captcha_validators = [DataRequired(), Length(min=6, max=6)]


class LoginForm(FlaskForm):
    username = StringField(label=u"Username", validators=username_validators)
    password = PasswordField(label=u"Password", validators=password_validators)
    submit = SubmitField(label=u"Login")

    def validate_password(self, password_field):
        user = User.query.filter_by(username=self.username.data).first()  # 查询原始密码
        if user:
            if user.status == 0:
                raise ValidationError("This account is currently inactive")
            if not check_password_hash(user.password, password_field.data):
                raise ValidationError('Password does not match')
        else:
            raise ValidationError('Username is invalid')


class PasswordResetRequestForm(FlaskForm):
    email = EmailField(label=u"Email Address", validators=email_validators)
    submit = SubmitField(label=u"Verify")

    def validate_email(self, email_field):
        if not User.query.filter_by(email=email_field.data).first():  # 邮箱不存在
            raise ValidationError('Email has not been registered')


class PasswordResetForm(FlaskForm):
    password = PasswordField(label=u"Password", validators=password_validators)
    submit = SubmitField(label=u"Confirm")


class AdminLoginForm(FlaskForm):
    username = StringField(label=u"Username", validators=username_validators)
    password = PasswordField(label=u"Password", validators=password_validators)
    submit = SubmitField(label=u"Login")

    def validate_password(self, password_field):
        admin = Admin.query.filter_by(username=self.username.data).first()  # 查询原始密码
        if admin:
            if admin.status == 0:
                raise ValidationError("This account is currently inactive")
            if not check_password_hash(admin.password, password_field.data):
                raise ValidationError('Password does not match')
        else:
            raise ValidationError('Username is invalid')


class RegisterForm(FlaskForm):
    username = StringField(label=u"Username", validators=username_validators)
    password = PasswordField(label=u"Password", validators=password_validators)
    email = EmailField(label=u"Email Address", validators=email_validators)
    captcha = StringField(label=u"Captcha", validators=captcha_validators)
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
