from door_api.extensions import db, ma
from door_api.database import Role


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role
        sqla_session = db.session
