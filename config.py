__author__ = 'JokerInteractive'
__email__ = 'info@jokerinteractive.ru'

CSRF_ENABLED = True
SECRET_KEY = 'c}Zfya3$#2&^M3N0X#V;'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://antipark:ways425_chic2@95.213.252.226/antipark'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = 'database'
ALLOWED_EXTENSIONS = set(['xlsx', 'xls'])

"""
MAIL_SERVER = 'smtp.yandex.ru'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'admin@jokerinteractive.ru'
MAIL_PASSWORD = 'Joker121212'

RESIZE_URL = '.'
RESIZE_ROOT = '.'
"""
DEBUG = True
