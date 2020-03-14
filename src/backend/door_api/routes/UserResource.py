from flask import Blueprint, abort, current_app, make_response, request
from flask.views import MethodView
from jose import jwt, JWTError
from webargs import fields
from webargs.flaskparser import parser

from door_api.database import Person
from door_api.models.JWTSchema import JWTSchema
from door_api.models.UserSchema import UserSchema

userBP = Blueprint('user', __name__, url_prefix='/user')
excludeFields = ['password', 'admin']
dumpSchema = UserSchema(exclude=excludeFields)
jwtSchema = JWTSchema()

loginSchema = {
    'username': fields.Str(required=True),
    'password': fields.Str(required=True)
}
# simple schema for handling code sent to url, probably will switch
# to custom header
codeSchema = {'token': fields.Str(required=True)}


class UserResource(MethodView):
    def _authenticatePassword(self, args):
        username = args['username']
        password = args['password']
        user = Person.query.filter_by(username=username).first_or_404()
        if (user.validatePassword(password)):
            token = jwt.encode(jwtSchema.dump(user),
                               current_app.config['SECRET_KEY'],
                               algorithm='HS256')
            return True, token
        else:
            return False, None

    def _authenticateJWT(self, username, args):
        token = args['token']
        try:
            decodedToken = jwt.decode(token, current_app.config['SECRET_KEY'])
            if decodedToken['username'] != username:
                return False, None
        except JWTError as err:
            return False, err
        return True, None

    def post(self, username):
        if username is None:
            # Password authentication
            args = parser.parse(loginSchema, request)
            success, token = self._authenticatePassword(args)
            if success is True:
                responseBody = {'meta': {'success': True}, 'token': token}
                response = make_response(responseBody)
                response.headers['X-Auth-Token'] = token
                return response
            else:
                abort(403, 'incorrect password')
        else:
            args = parser.parse(codeSchema, request)
            success, data = self._authenticateJWT(username, args)
            if success is True:
                responseBody = {
                    'meta': {
                        'success': True,
                        'message': 'valid token'
                    }
                }
                return responseBody
            else:
                abort(403, getattr(data, 'description', 'invalid token'))


userView = UserResource.as_view('user')
userBP.add_url_rule('',
                    'UserResource',
                    defaults={'username': None},
                    view_func=userView)
userBP.add_url_rule('/<username>/code', 'UserResource', view_func=userView)
