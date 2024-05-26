SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000

DATABASE_USERNAME = 'root'
DATABASE_PASSWORD = '1234'
DATABASE_HOST = 'mysql'
DATABASE_PORT = 3306
DATABASE = 'deeplearning_gallery'
DATABASE_URI = f'mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DATABASE_URI

IDCARD_SCANNER_HOST = 'idcardscanner'
IDCARD_SCANNER_PORT = 5000

REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_PASSWORD = ''

SECRET_KEY = 'Pineclone'

PANEL_ICON_DIR = 'static/images'

MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_SERVER = ''
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
MAIL_DEFAULT_SENDER = ''
