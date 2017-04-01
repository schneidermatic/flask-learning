from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Configuration 

SQLALCHEMY_TRACK_MODIFICATIONS=True

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_object(Configuration)
db = SQLAlchemy(app)
