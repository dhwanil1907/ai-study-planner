from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    plans = db.relationship('StudyPlan', backref='user', lazy=True)

class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subjects = db.Column(db.String(500), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    hours_per_day = db.Column(db.Integer, nullable=False)
    schedule = db.Column(db.Text, nullable=False)  # JSON string of the schedule
    progress = db.relationship('Progress', backref='study_plan', lazy=True)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    study_plan_id = db.Column(db.Integer, db.ForeignKey('study_plan.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)