from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    password = db.Column(db.String, nullable=False)
    person = db.relationship('Person')
