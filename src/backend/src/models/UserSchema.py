from src.extensions import db, ma
from src.database.Person import Person


class UserSchema(ma.ModelSchema):
    class Meta:
        model = Person
        fields = ('firstName', 'lastName', 'username', 'password', 'addedBy')
        sqla_session = db.session
