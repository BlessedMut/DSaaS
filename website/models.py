from email.policy import default
from enum import unique
from time import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Regression(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Classification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Clustering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    address = db.Column(db.String(500))
    phone_number = db.Column(db.String(15))
    country = db.Column(db.String(50))
    company = db.Column(db.String(100))
    profession = db.Column(db.String(100))
    regression_model = db.relationship('Regression')
    classification_model = db.relationship('Classification')
    clustering_model = db.relationship('Clustering')