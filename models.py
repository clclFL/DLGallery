from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from exts import db


class User(db.Model):
    __tablename__ = 'db_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    create_time = Column(DateTime, default=datetime.now)
