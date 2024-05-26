import os

from flask import Flask, send_from_directory, session, g
from flask_migrate import Migrate

import config
from blueprints.auth import bp as auth_bp
from blueprints.index import bp as index_bp
from blueprints.gallery import bp as gallery_bp
from blueprints.admin import bp as admin_bp
from blueprints.user import bp as user_bp
from exts import db, mail
from models import User, Admin

app = Flask(__name__)  # 项目主路由
app.config.from_object(config)  # 加载外部配置
db.init_app(app)  # 初始化数据库连接
mail.init_app(app)  # 邮件服务初始化

migrate = Migrate(app, db)  # ORM模型映射

app.register_blueprint(auth_bp)  # 路由注册
app.register_blueprint(index_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)


@app.route('/favicon.ico')  # 项目图标
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'images/favicon.ico', mimetype='image/vnd.microsoft.icon')


# 请求执行之前通过user_id绑定用户对象到全局
@app.before_request
def prj_before_request():
    user_id = session.get('user_id')

    if user_id is None:
        setattr(g, 'user', None)
    else:
        user = User.query.get(user_id)
        if user and user.status == 0:  # 如果账户此时处于禁用状态
            del session['user_id']
            setattr(g, 'user', None)
        else:
            setattr(g, 'user', user)

    admin_id = session.get('admin_id')
    if admin_id is None:
        setattr(g, 'admin', None)
    else:
        admin = Admin.query.get(admin_id)
        if admin and admin.status == 0:  # 如果账户此时处于禁用状态
            del session['admin_id']
            setattr(g, 'admin', None)
        else:
            setattr(g, 'admin', admin)


# 将全局对象中的user对象获取到上下文中，上下文中的数据在所有模板中都能够使用
@app.context_processor
def prj_context_processor():
    return {'user': g.user, 'admin': g.admin}


if __name__ == '__main__':
    app.run(host=config.SERVER_HOST, port=config.SERVER_PORT)
