from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import config
import redis

db = SQLAlchemy()
mail = Mail()
r = redis.StrictRedis(host=config.REDIS_HOST,
                      port=config.REDIS_PORT,
                      db=config.REDIS_DB,
                      password=config.REDIS_PASSWORD,
                      decode_responses=True)
