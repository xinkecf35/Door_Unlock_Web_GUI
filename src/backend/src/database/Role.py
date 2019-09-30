from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Role(db.Model):
    id = db.Column('role_id', db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    canUnlock = db.Column('can_unlock', db.Integer)
    canManage = db.Column('can_manage', db.Integer)
    canAccessHistory = db.Column('can_access_history', db.Integer)

    def __repr__(self):
        return f'role: role_id:{id}, name: {name}'

    def __str__(self):
        return f'role name: {name}'
