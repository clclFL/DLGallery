from flask import Blueprint, render_template, g, redirect, url_for, request
from sqlalchemy.sql.functions import current_user

from decorators import login_required
from exts import db
from models import ModelPanel, UserLikesModel

bp = Blueprint('gallery', __name__, url_prefix='/gallery')


@bp.route('/models')
@login_required
def gallery():
    # 查询数据库
    query = ModelPanel.query.all()
    panels = []
    for panel in query:
        if panel.status == 1:  # 判断是否激活
            panels.append({
                'id': panel.id,
                'title': panel.title,
                'icon': panel.icon,
                'inner': panel.inner,
                'banner': panel.banner,
                'likes': panel.likes
            })
    return render_template('gallery.html', panels=panels)


@bp.route('/models/<int:panel_id>')
@login_required
def panelDetail(panel_id):
    # 查询数据库
    user_like_model = UserLikesModel.query.filter_by(modelpanel_id=panel_id, user_id=g.user.id).first()
    like = False
    if user_like_model:
        like = True
    panel = ModelPanel.query.get(panel_id)
    return render_template(f'modelPanel/{panel_id}.html',
                           panel=panel, admin=panel.admin, like=like)


@bp.route('/models/likes')
@login_required
def panelLikes():
    modelpanel_id = request.args.get('modelpanel_id')
    user_like_model = UserLikesModel.query.filter_by(modelpanel_id=modelpanel_id, user_id=g.user.id).first()
    if user_like_model:
        # 删除喜欢
        db.session.delete(user_like_model)
        modelpanel = ModelPanel.query.get(modelpanel_id)
        modelpanel.likes -= 1
        db.session.commit()
    else:
        # 创建喜欢
        user_like_model = UserLikesModel()
        modelpanel = ModelPanel.query.get(modelpanel_id)
        user_like_model.user = g.user
        user_like_model.modelpanel = modelpanel
        db.session.add(user_like_model)

        modelpanel = ModelPanel.query.get(modelpanel_id)
        modelpanel.likes += 1
        db.session.commit()

    return redirect(url_for('gallery.panelDetail', panel_id=modelpanel_id))