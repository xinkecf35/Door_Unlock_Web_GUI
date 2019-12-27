from src.extensions import db, ma
from src.database.Role import Role


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role
        sqla_session = db.session
