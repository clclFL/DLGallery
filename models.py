from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from exts import db


class User(db.Model):
    """ 用户 """
    __tablename__ = 'db_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    status = Column(Integer, nullable=False, default=lambda: 1)  # 状态
    create_time = Column(DateTime, default=datetime.now)


class Admin(db.Model):
    """ 管理员 """
    __tablename__ = 'db_admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    permission = Column(Integer, nullable=False, default=lambda: 0)  # 权限
    status = Column(Integer, nullable=False, default=lambda: 1)  # 状态
    create_time = Column(DateTime, default=datetime.now)


class ModelPanel(db.Model):
    """ 模型嵌板 """
    __tablename__ = 'db_modelpanel'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False, unique=True)  # 标题
    banner = Column(String(255), nullable=False)  # 旗帜
    inner = Column(String(255), nullable=False)  # 内容
    icon = Column(String(255))  # 图标
    likes = Column(Integer, nullable=False, default=lambda: 0)  # 推荐
    status = Column(Integer, nullable=False, default=lambda: 0)  # 状态
    create_time = Column(DateTime, default=datetime.now)

    admin_id = db.Column(db.Integer, db.ForeignKey('db_admin.id'))
    admin = db.relationship(Admin, backref='model_panels')



