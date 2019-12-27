from base64 import b64encode
import bcrypt
from datetime import datetime
from hashlib import sha256
from src.extensions import db
from sqlalchemy import event


def encodePassword(input):
    passwordBytes = bytes(input, encoding='UTF-8')
    return b64encode(sha256(passwordBytes).digest())


class Person(db.Model):
    id = db.Column('person_id', db.Integer, primary_key=True)
    firstName = db.Column('first_name', db.String(50), nullable=False)
    lastName = db.Column('last_name', db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    created = db.Column(db.DateTime(), default=datetime.utcnow())
    addedBy = db.Column(
        'added_by',
        db.Integer,
        db.ForeignKey('person.person_id'))
    password = db.Column(db.LargeBinary(60), nullable=False)
    roleId = db.Column(
        'role',
        db.Integer,
        db.ForeignKey("role.role_id"),
        default='1')
    role = db.relationship('Role')
    admin = db.relationship('Person')

    def validatePassword(self, password):
        encodedPassword = encodePassword(password)
        return bcrypt.checkpw(encodedPassword, self.password)

    def __repr__(self):
        return f'Person: user_id:{id}, name: {self.lastName};{self.firstName}'

    def __str__(self):
        return f'Name: {self.firstName} {self.lastName}'


@event.listens_for(Person, 'before_insert')
@event.listens_for(Person, 'before_update')
def hashPassword(mapper, connect, person):
    encodedPassword = encodePassword(person.password)
    person.password = bcrypt.hashpw(encodedPassword, bcrypt.gensalt())
