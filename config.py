import os


class Config:
    SECRET_KEY = '7ac934cde24f13bb1b60c2329ee8d9fd'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_KEY = '123AB'
