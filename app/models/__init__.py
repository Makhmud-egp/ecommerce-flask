from enum import unique

from app import db
from datetime import datetime

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50))
    created_at = db.Column(db.Datetime, default=datetime.utcnow())

    def __repr__(self):
        return f'<User {self.email}>'