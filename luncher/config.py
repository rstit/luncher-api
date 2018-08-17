import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///luncher.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = True
