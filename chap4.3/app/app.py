from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask_sqlalchemy import SQLAlchemy

from config import Configuration 

SQLALCHEMY_TRACK_MODIFICATIONS=True

app = Flask(__name__)
#app = Flask(__name__, template_folder="views")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
