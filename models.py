from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class flags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.String(200))
    help = db.Column(db.String(200))
    points = db.Column(db.Integer)

