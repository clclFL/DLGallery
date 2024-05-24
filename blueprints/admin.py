import os
import uuid

from flask import Blueprint, render_template, session, request, redirect, url_for, g
from pyecharts.charts import Bar, Line
from pyecharts.globals import ThemeType
from pyecharts.options import TextStyleOpts, LineStyleOpts
from werkzeug.utils import secure_filename

import config
from exts import db
from models import Admin, User, ModelPanel
from .forms import AdminLoginForm, ModelPanelForm, ModelPanelModifyForm
from decorators import admin_required
from pyecharts import options as opts

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=['GET', 'POST'])
def admin():
    form = AdminLoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            admin = Admin.query.filter_by(username=username).first()
            session['admin_id'] = admin.id
            return redirect('/admin/analyze')
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


@bp.get('/analyze')
@admin_required
def analyze():
    return render_template('admin/dataManagement.html')


@bp.get('/userAccounts')
@admin_required
def userAccounts():
    # 查询数据库
    query = User.query.all()
    users = []
    for user in query:
        users.append({
            'id': user.id,
            'username': user.username,
            'status': 'Active' if user.status == 1 else 'Inactive',
        })
    return render_template('admin/userManagement.html', users=users)


@bp.get('/modelPanels')
@admin_required
def modelPanels():
    # 查询数据库
    query = ModelPanel.query.all()
    form = ModelPanelForm()  # 创建model panel
    panels = []
    for panel in query:
        panels.append({
            'id': panel.id,
            'title': panel.title,
            'icon': panel.icon,
            'status': 'Active' if panel.status == 1 else 'Inactive',
        })
    traceback = request.args.get('traceback')
    return render_template('admin/modelManagement.html',
                           panels=panels, form=form, traceback=traceback)


@bp.route('/modelPanels/<int:panel_id>', methods=('GET', 'POST'))
@admin_required
def modifyModelPanels(panel_id):
    if request.method == 'GET':
        panel = ModelPanel.query.get(panel_id)  # 查询数据库
        form = ModelPanelModifyForm(obj=panel)  # 创建model panel

        traceback = request.args.get('traceback')
        return render_template('admin/modelCheck.html',
                               panel=panel, form=form, traceback=traceback)
    else:  # 修改单条数据
        form = ModelPanelModifyForm()
        title = form.title.data
        banner = form.banner.data
        inner = form.inner.data
        status = form.status.data
        icon_file = form.icon.data

        modelPanel = ModelPanel.query.get(panel_id)
        modelPanel.title = title
        modelPanel.banner = banner
        modelPanel.inner = inner
        modelPanel.status = status

        if icon_file:
            base, ext = os.path.splitext(secure_filename(icon_file.filename))
            icon_filename = f'{uuid.uuid4().hex}.{ext}'
            icon_file.save(os.path.join(config.PANEL_ICON_DIR, icon_filename))  # 保存文件
            modelPanel.icon = f'images/{icon_filename}'

        db.session.commit()  # 提交修改
        return redirect(url_for('admin.modifyModelPanels', panel_id=panel_id))


font_options = opts.LabelOpts(color='#dee2e6', font_family='Consolas, monospace', font_size=16)


def apiBar():
    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.DARK, ))
        .add_xaxis(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        .add_yaxis("requests", [820, 932, 901, 934, 1290, 1330, 1320],
                   label_opts=opts.LabelOpts(color='#f8c4f7', font_family='Consolas, monospace', font_size=14),
                   linestyle_opts=opts.LineStyleOpts(color='#f8c4f7'))
        .add_yaxis("likes", [15, 25, 30, 18, 65, 70, 32],
                   label_opts=opts.LabelOpts(color='#00aa00', font_family='Consolas, monospace', font_size=14),
                   linestyle_opts=opts.LineStyleOpts(color='#00aa00'),
                   )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=font_options),
            yaxis_opts=opts.AxisOpts(axislabel_opts=font_options),
            title_opts=opts.TitleOpts(title="API Data",
                                      title_textstyle_opts=TextStyleOpts(color="white")),
            legend_opts=opts.LegendOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(is_show=True)
        )
    )
    return line


@bp.route("/modelPanels/aptChart")
@admin_required
def getApiChart():
    c = apiBar()
    return c.dump_options_with_quotes()


@bp.route("/modelPanels/delete")
@admin_required
def deleteModelPanel():
    delete_id = request.args.get("delete_id")
    delete = ModelPanel.query.get(delete_id)
    db.session.delete(delete)
    db.session.commit()
    traceback = 'delete success'
    return redirect(url_for('admin.modelPanels', traceback=traceback))


@bp.post('/modelPanels')
@admin_required
def addModelPanel():
    # 查询数据库
    form = ModelPanelForm()
    if form.validate():
        title = form.title.data
        banner = form.banner.data
        icon_file = form.icon.data

        base, ext = os.path.splitext(secure_filename(icon_file.filename))
        icon_filename = f'{uuid.uuid4().hex}.{ext}'
        icon_file.save(os.path.join(config.PANEL_ICON_DIR, icon_filename))  # 保存文件

        inner = form.inner.data
        pannel = ModelPanel(title=title, banner=banner, icon=f'images/{icon_filename}', inner=inner, admin=g.admin)
        db.session.add(pannel)
        db.session.commit()
        return redirect(url_for('admin.modelPanels'))
    else:
        reason = []
        for k, v in form.errors.items():
            reason.append(", ".join(v))
        return redirect(url_for('admin.modelPanels', traceback=", ".join(reason)))
