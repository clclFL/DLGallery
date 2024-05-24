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

bp = Blueprint('users', __name__, url_prefix='/users')


