from src.extensions import db, ma
from src.database.Person import Person
from src.models.RoleSchema import RoleSchema


class UserSchema(ma.ModelSchema):
    class Meta:
        model = Person
        sqla_session = db.session
    role = ma.Nested(RoleSchema)
