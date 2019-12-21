from src.extensions import ma
from src.database.Person import Person


class UserSchema(ma.ModelSchema):
    class Meta:
        model = Person
        fields = ('firstName', 'lastName', 'username', 'addedBy')
