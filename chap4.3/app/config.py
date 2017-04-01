import os

class Configuration(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    SECRET_KEY = 'flask is fun!'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/flask_db'
