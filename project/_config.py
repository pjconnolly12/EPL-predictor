import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'predictor.db'
CSRF_ENABLED = True
SECRET_KEY = 'soccer'
DEBUG = True

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH