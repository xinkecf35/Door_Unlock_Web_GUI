from src.extensions import db


class Admin(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    password = db.Column(db.String, nullable=False)
    person = db.relationship('Person', useList=False)
