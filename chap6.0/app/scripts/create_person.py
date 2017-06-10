import os, sys

sys.path.append(os.getcwd())

from app import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import db
from models import *

if __name__ == '__main__':
    persons = [Person(email='charlie@gmail.com', password_hash=bcrypt.generate_password_hash("secret"), name="charlie")
    ]

    db.session.add_all(persons)
    db.session.commit()

    db.session.close()
