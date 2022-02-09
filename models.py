from unicodedata import category
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(200))
    name = db.Column(db.String(200))
    category = db.Column(db.String(200))
    difficulty = db.Column(db.String(200))
    status = db.Column(db.String(200))
    url = db.Column(db.String(200))
    flags = db.relationship('Flags', backref='game')

class Flags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.String(200))
    hint = db.Column(db.String(200))
    points = db.Column(db.Integer)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))


