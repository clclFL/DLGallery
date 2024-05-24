import random
import re
import uuid
from datetime import datetime
from string import digits

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from flask_mail import Message
from werkzeug.security import generate_password_hash  # 加密、解密

from exts import mail, r, db
from models import User
from .forms import LoginForm, RegisterForm, PasswordResetRequestForm, PasswordResetForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate():
            # post请求下
            username = form.username.data
            password = generate_password_hash(form.password.data)
            email = form.email.data
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('auth.registerSuccess'))
        else:
            reason = []
            for k, v in form.errors.items():
                reason.append(", ".join(v))
            return render_template('fail.html', title='Register Fail', reason=", ".join(reason))
    else:
        return render_template("register.html", form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            user = User.query.filter_by(username=username).first()
            session['user_id'] = user.id
            return redirect('/')
        else:
            reason = []
            for k, v in form.errors.items():
                reason.append(", ".join(v))
            return render_template('fail.html', title='Login Fail', reason=", ".join(reason))
    else:
        return render_template("login.html", form=form)


@bp.post('/email/captcha')
def send_email():
    email = request.json.get('email')
    if not email:
        return jsonify({
            'code': 400,
            'message': 'Email address cannot be empty',
        })

    pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+$'  # 匹配邮箱
    if not re.match(pattern, email):
        return jsonify({
            'code': 400,
            'message': 'Bad email address format',
        })

    # 生成验证码
    seed = random.sample(digits, 6) * 6
    captcha = "".join(random.sample(seed, 6))
    formatted_date = datetime.now().strftime("%Y-%m-%d")

    title = '深度学习画廊 - 请验证您的电子邮箱'
    body = f'''
    您好！
    您收到此邮件是因为有人在我们的平台上使用了您的电子邮箱地址进行了账户验证请求。请忽略此邮件，如果这不是您本人的操作。
    如果您本人请求了此验证邮件，请在以下验证码输入框中输入以下验证码：
    
    验证码：{captcha}
    
    请在收到此邮件后的5分钟内输入验证码进行验证。请勿将此验证码泄露给任何其他人。
    如果您没有请求此验证邮件，请忽略此邮件。
    
    来自：Pineclone
    {formatted_date}
    '''
    # 储存验证码并设置过期时间
    r.set(email, captcha, 300)
    message = Message(subject=title, recipients=[email], body=body)
    mail.send(message)
    return jsonify({
        'code': 200,
        'message': 'mail sending successfully',
        'data': email
    })


# todo: add feedback
@bp.get('/feedback')
def feedback():
    return render_template('feedback.html')


@bp.get('/registerSuccess')
def registerSuccess():
    return render_template('registerSuccess.html')


@bp.get('/logout')
def logout():
    if session['user_id']:
        del session['user_id']
    return redirect('/')


@bp.route('/password/reset/request', methods=['GET', 'POST'])
def requestPasswordReset():
    form = PasswordResetRequestForm()
    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            token = uuid.uuid4().hex
            url = f'http://{request.host}/auth/password/reset/{token}'
            formatted_date = datetime.now().strftime("%Y-%m-%d")

            title = '深度学习画廊 - 重置您的账户密码'
            body = f'''
            您好！
            您收到此邮件是因为有人在我们的平台上使用了您的电子邮箱地址进行了重置密码请求，如果这不是您本人所操作，请您
            忽略该邮件，如果需要重置密码，请点击下方链接进入密码重置页面

            重置密码链接: {url}

            请在收到此邮件后的5分钟内输入验证码进行验证。请勿将此验证码泄露给任何其他人。
            如果您没有请求此验证邮件，请忽略此邮件。

            来自：Pineclone
            {formatted_date}
            '''
            # 储存验证码并设置过期时间
            r.set(token, email, 300)
            message = Message(subject=title, recipients=[email], body=body)
            mail.send(message)

            return render_template('passwordResetVerified.html', email=email)
        else:
            reason = []
            for k, v in form.errors.items():
                reason.append(", ".join(v))
            return render_template('fail.html', title='Reset Password Fail', reason=", ".join(reason))
    else:
        return render_template("passwordResetRequest.html", form=form)


@bp.route('password/reset/<token>', methods=["GET", "POST"])
def passwordResetToken(token):
    if not r.exists(token):
        return render_template('fail.html', title='Reset Password Fail', reason='Token has expired.')
    form = PasswordResetForm()
    if request.method == 'GET':
        email = r.get(token)
        return render_template("passwordReset.html", form=form, token=token, email=email)
    else:
        if form.validate():
            email = r.get(token)
            user = User.query.filter_by(email=email).first()
            user.password = generate_password_hash(form.password.data)
            db.session.commit()  # 更新数据
            return render_template('passwordResetSuccess.html', email=email)
        else:
            reason = []
            for k, v in form.errors.items():
                reason.append(", ".join(v))
            return render_template('fail.html', title='Login Fail', reason=", ".join(reason))



