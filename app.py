import os

from flask import Flask, send_from_directory
from flask_migrate import Migrate

import config
from blueprints.auth import bp as auth_bp
from blueprints.index import bp as index_bp
from exts import db, mail

app = Flask(__name__)  # 项目主路由
app.config.from_object(config)  # 加载外部配置
db.init_app(app)  # 初始化数据库连接
mail.init_app(app)  # 邮件服务初始化

migrate = Migrate(app, db)  # ORM模型映射

app.register_blueprint(auth_bp)  # 路由注册
app.register_blueprint(index_bp)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'images/favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run()
