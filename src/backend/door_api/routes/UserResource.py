from flask import Blueprint, current_app
from flask.views import MethodView
from jose import jwt
from webargs import fields
from webargs.flaskparser import use_args

from door_api.database import Person
from door_api.extensions import db
from door_api.models.UserSchema import UserSchema

userBP = Blueprint('user', __name__, url_prefix='/user')
excludeFields = ['password', 'admin']
dumpSchema = UserSchema(exclude=excludeFields)

loginSchema = {
    'username': fields.Str(required=True),
    'password': fields.Str(required=True)
}


class UserResource(MethodView):

    @use_args(loginSchema)
    def post(self, args):
        username = args['username']
        password = args['password']
        user = Person.query.filter_by(username=username).first_or_404()
        if (user.validatePassword(password)):
            token = jwt.encode(
                dumpSchema.dump(user),
                current_app.config['SECRET_KEY'],
                algorithm='HS256')
            return {'meta': {'success': True}, 'token': token}


userBP.add_url_rule('', 'UserResource', view_func=UserResource.as_view('user'))
