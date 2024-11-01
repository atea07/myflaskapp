import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'da6b8d2db10a946548c6b1d649ed578c'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sites.db'