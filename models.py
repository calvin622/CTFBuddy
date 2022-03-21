from unicodedata import category
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    image = db.Column(db.String(100), unique=True)
    games = db.relationship('Games', backref='user')
    points = db.Column(db.Integer)
    usergamestatus = db.relationship('UserGameStatus', backref='user')

class UserGameStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(200))
    flag1_status = db.Column(db.String(200))
    flag2_status = db.Column(db.String(200))
    flag3_status = db.Column(db.String(200))
    flag4_status = db.Column(db.String(200))
    flag5_status = db.Column(db.String(200))
    flag6_status = db.Column(db.String(200))
    flag7_status = db.Column(db.String(200))
    flag8_status = db.Column(db.String(200))
    flag9_status = db.Column(db.String(200))
    flag10_status = db.Column(db.String(200))
    hint1_status = db.Column(db.String(200))
    hint2_status = db.Column(db.String(200))
    hint3_status = db.Column(db.String(200))
    hint4_status = db.Column(db.String(200))
    hint5_status = db.Column(db.String(200))
    hint6_status = db.Column(db.String(200))
    hint7_status = db.Column(db.String(200))
    hint8_status = db.Column(db.String(200))
    hint9_status = db.Column(db.String(200))
    hint10_status = db.Column(db.String(200))
    video_status = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    games_name = db.Column(db.String(200), db.ForeignKey('games.name'))

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(200))
    category = db.Column(db.String(200))
    difficulty = db.Column(db.String(200))
    url = db.Column(db.String(200))
    video_url = db.Column(db.String(200))
    video_cost = db.Column(db.Integer)
    image = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    usergamestatus = db.relationship('UserGameStatus', backref='games')
    flags = db.relationship('Flags', backref='games')


class Flags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flag_num = db.Column(db.Integer)
    flag = db.Column(db.String(200))
    hint = db.Column(db.String(200))
    hint_cost = db.Column(db.Integer)
    points = db.Column(db.Integer)
    games_name = db.Column(db.String(200), db.ForeignKey('games.name'))
