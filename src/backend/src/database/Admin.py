from src.extensions import db


class Admin(db.Model):
    id = db.Column(
        'admin_id',
        db.Integer,
        db.ForeignKey('person.person_id'),
        primary_key=True)
    password = db.Column(db.String, nullable=False)
    person = db.relationship('Person', uselist=False)
