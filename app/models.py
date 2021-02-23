import datetime

from . import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON


class AccessLog(db.Model):
    __tablename__ = "access_logs"

    id = db.Column(db.Integer, primary_key=True)
    request_body = db.Column(JSON, nullable=True)
    response_body = db.Column(JSON, nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, request_body, response_body):
        self.request_body = request_body
        self.response_body = response_body

    def __repr__(self):
        return str(created_on)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def list_all(cls):
        access_logs = cls.query.all()

        return [
            {
                "id": access_log.id,
                "request_body": access_log.request_body,
                "response_body": access_log.response_body,
                "created_on": str(access_log.created_on),
            }
            for access_log in access_logs
        ]
