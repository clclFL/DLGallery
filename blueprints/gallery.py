import base64
import json
import os
import uuid

import requests
from flask import Blueprint, render_template, g, redirect, url_for, request, jsonify
from sqlalchemy.sql.functions import current_user

import config
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
    url = f'modelPanel/{panel.forward}.html'
    return render_template(url, panel=panel, admin=panel.admin, like=like)


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


@bp.route('/models/idcardscanning', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']

    # 将文件发送到第二个Flask应用
    url = f'http://{config.IDCARD_SCANNER_HOST}:{config.IDCARD_SCANNER_PORT}/idcardscanning/analyzeBorder'

    # data = {'file': open('/path-to-your-file/test.doc', 'rb')}
    data = {'file': file}
    response = requests.post(url, files=data)

    # headers = {'Content-Type': file.content_type}
    # response = requests.post(url, files={'file': file}, headers=headers)

    if response.status_code == 200:
        data = base64.b64decode(response.content)
        image_name = uuid.uuid4().hex + '.jpg'
        url = 'static/images/handle_images/' + image_name
        with open(url, 'wb') as f:
            f.write(data)
        return jsonify({'message': 'File processed successfully', 'data': f'images/handle_images/{image_name}'}), 200
    else:
        return jsonify({'error': 'Failed to process file'}), 500


@bp.route('/models/analyzeText', methods=['POST'])
@login_required
def analyzeText():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']

    # 将文件发送到第二个Flask应用
    url = f'http://{config.IDCARD_SCANNER_HOST}:{config.IDCARD_SCANNER_PORT}/idcardscanning/analyzeText'

    # data = {'file': open('/path-to-your-file/test.doc', 'rb')}
    data = {'file': file}
    response = requests.post(url, files=data)

    if response.status_code == 200:
        data = base64.b64decode(response.content)
        image_name = uuid.uuid4().hex + '.jpg'
        url = 'static/images/handle_images/' + image_name
        with open(url, 'wb') as f:
            f.write(data)
        return jsonify({'message': 'File processed successfully', 'data': f'images/handle_images/{image_name}'}), 200
    else:
        return jsonify({'error': 'Failed to process file'}), 500


@bp.route('/models/getText', methods=['POST'])
@login_required
def getText():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']

    # 将文件发送到第二个Flask应用
    url = f'http://{config.IDCARD_SCANNER_HOST}:{config.IDCARD_SCANNER_PORT}/idcardscanning/getText'

    data = {'file': file}
    response = requests.post(url, files=data)

    if response.status_code == 200:
        data = json.loads(response.content)
        return jsonify({'message': 'File processed successfully', 'data': data}), 200
    else:
        return jsonify({'error': 'Failed to process file'}), 500

