from datetime import datetime
from src.extensions import db


class Person(db.Model):
    id = db.Column('person_id', db.Integer, primary_key=True)
    firstName = db.Column('first_name', db.String(50), nullable=False)
    lastName = db.Column('last_name', db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    created = db.Column(db.DateTime(), default=datetime.utcnow())
    addedBy = db.Column('added_by', db.Integer)
    role = db.Column('role',
                     db.Integer,
                     db.ForeignKey("role.role_id"),
                     default='1')

    def __repr__(self):
        return f'Person: user_id:{id}, name: {self.lastName};{self.firstName}'

    def __str__(self):
        return f'Name: {self.firstName} {self.lastName}'
