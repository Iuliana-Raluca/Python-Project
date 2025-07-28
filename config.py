import secrets

class Config:
    SECRET_KEY = '7ac934cde24f13bb1b60c2329ee8d9fd'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = "123AB"