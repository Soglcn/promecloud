"""
Define the Project data model representing files and metadata stored in the database.
"""


from app import db
from datetime import datetime

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    keywords = db.Column(db.String(255))
    filename = db.Column(db.String(255))
    filetype = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
