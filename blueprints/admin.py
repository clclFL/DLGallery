from flask import Blueprint, render_template, session, request, redirect, url_for
from models import Admin
from .forms import AdminLoginForm

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=['GET', 'POST'])
def admin():
    form = AdminLoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            admin = Admin.query.filter_by(username=username).first()
            session['admin_id'] = admin.id
            return redirect('/admin')
        else:
            reason = []
            for k, v in form.errors.items():
                reason.append(", ".join(v))
            return render_template('admin/fail.html', title='Login Fail', reason=", ".join(reason))
    else:
        return render_template("admin/index.html", form=form)


@bp.get('/logout')
def logout():
    if session['admin_id']:
        del session['admin_id']
    return redirect('/admin')
