from src.extensions import db


class Role(db.Model):
    id = db.Column('role_id', db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False, unique=True)
    canUnlock = db.Column('can_unlock', db.Integer)
    canManage = db.Column('can_manage', db.Integer)
    canAccessHistory = db.Column('can_access_history', db.Integer)
