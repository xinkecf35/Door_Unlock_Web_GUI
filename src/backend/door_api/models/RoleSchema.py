from door_api.extensions import db, ma
from door_api.database import Role


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        sqla_session = db.session
        load_instance = True
        include_relationships = True
