from door_api.extensions import db
from datetime import datetime


class Event(db.Model):
    id = db.Column('event_id', db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    time = db.Column(db.DateTime(), default=datetime.utcnow())
    user = db.Column(db.Integer, db.ForeignKey('person.person_id'))
