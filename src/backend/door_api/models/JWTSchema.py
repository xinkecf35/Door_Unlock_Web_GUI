from marshmallow import fields

from door_api.database import Person
from door_api.extensions import db, ma

from .RoleSchema import RoleSchema


class JWTSchema(ma.ModelSchema):
    sub = fields.String(attribute='username')
    role = ma.Nested(RoleSchema, only=['id', 'name'], partial=True)

    class Meta:
        model = Person
        exclude = [
            'username',
            'id',

            'created',
            'addedBy',
            'admin',
            'password'
        ]
        sqla_session = db.session
