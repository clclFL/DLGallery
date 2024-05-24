from functools import wraps
from flask import g, redirect, url_for


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        else:
            return func(*args, **kwargs)
    return inner


def admin_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.admin is None:
            return redirect(url_for('admin.admin'))
        else:
            return func(*args, **kwargs)
    return inner
