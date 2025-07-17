from . import db
from datetime import datetime, timezone


class OperationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(50))
    input_data = db.Column(db.Text)
    result = db.Column(db.Text)
    status_code = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
