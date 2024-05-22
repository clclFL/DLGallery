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
