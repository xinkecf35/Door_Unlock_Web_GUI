from src.extensions import db
from sqlalchemy import event


class Role(db.Model):
    id = db.Column('role_id', db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    canUnlock = db.Column('can_unlock', db.Integer)
    canManage = db.Column('can_manage', db.Integer)
    canAccessHistory = db.Column('can_access_history', db.Integer)
    persons = db.relationship('Person', lazy='joined')
