from app import db
from datetime import datetime


class Companies(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(120), nullable=False, unique=True)
   description = db.Column(db.Text, nullable=False)
   url = db.Column(db.Text, nullable=False, unique=True)
   positions = db.relationship('Positions', lazy=True, backref='Companies')


class Positions(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(120), nullable=False)
   division = db.Column(db.String(120), nullable=False)
   role = db.Column(db.String(120), nullable=False)
   location = db.Column(db.String(120), nullable=False)
   timescale = db.Column(db.String(80), nullable=False)
   date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
   company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
   url = db.Column(db.Text, nullable=False)
