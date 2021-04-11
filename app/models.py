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
   description = db.Column(db.String(1000), nullable=False)
   role = db.Column(db.String(120), nullable=False)            # [categorical] IB, Tech, etc.
   location = db.Column(db.String(120), nullable=False)
   job_type = db.Column(db.String(80), nullable=False)        # [categorical] Internship, graduate, etc.
   date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
   date_closing = db.Column(db.DateTime, nullable=False)
   company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
   url = db.Column(db.Text, nullable=False)
