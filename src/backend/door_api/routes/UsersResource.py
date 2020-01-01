from flask import Blueprint, abort, request
from flask.views import MethodView
from marshmallow import ValidationError
from webargs.flaskparser import use_args

from door_api.extensions import db
from door_api.models.UserSchema import UserSchema

from .JSONResponse import JSONResponse

usersBP = Blueprint('users', __name__, url_prefix='/users')
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
        return {'meta': {'success': True}, 'user': user}


usersBP.add_url_rule(
    '',
    'UsersResource',
    view_func=UsersResource.as_view('users')
)
