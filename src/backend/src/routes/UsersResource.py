from flask import abort, Blueprint, request
from .JSONResponse import JSONResponse
from flask.views import MethodView
from marshmallow import ValidationError
from src.extensions import db
from src.models.UserSchema import UserSchema
from webargs.flaskparser import parser, use_args

bp = Blueprint('users', __name__, url_prefix='/users')
excludeFields = ['password', 'admin']
schema = UserSchema()
dumpSchema = UserSchema(exclude=excludeFields)


class UsersResource(MethodView):
    response_class = JSONResponse

    @use_args(UserSchema(), locations=['json'])
    def post(self, newUser):
        try:
            db.session.add(newUser)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)
        user = dumpSchema.dump(newUser)
        return {'user': user}


bp.add_url_rule('', 'UsersResource', view_func=UsersResource.as_view('users'))
