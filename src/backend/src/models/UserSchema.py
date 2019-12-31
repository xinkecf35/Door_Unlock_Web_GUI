from src.extensions import db, ma
from src.database.Person import Person
from src.database.Role import Role
from marshmallow import fields, ValidationError
from .RoleSchema import RoleSchema


def _checkRoleExistence(role):
    if role is not None:
        roleId = role.id
        if Role.query.filter_by(id=roleId).first() is None:
            raise ValidationError(f'role does not exists')


class AddedByField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ''
        addedByPerson = Person.query.filter_by(id=value).first()
        return addedByPerson.username

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        addedByPerson = Person.query.filter_by(username=value).first()
        if addedByPerson is None:
            raise ValidationError('user does not exists')
        return addedByPerson.id


class UserSchema(ma.ModelSchema):
    class Meta:
        model = Person
        sqla_session = db.session

    addedBy = AddedByField()
    role = ma.Nested(
        RoleSchema,
        only=['id', 'name'],
        partial=True,
        validate=_checkRoleExistence)
