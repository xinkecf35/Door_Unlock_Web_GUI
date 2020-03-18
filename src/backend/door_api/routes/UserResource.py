import qrcode
from io import BytesIO
from flask import (Blueprint, abort, current_app, make_response, send_file,
                   request)
from flask.views import MethodView
from jose import JWTError, jwt
from webargs import fields
from webargs.flaskparser import parser, use_args

from door_api.database import Person
from door_api.decorators import tokenRequired
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

    @use_args(loginSchema)
    def post(self, args):
        # Password authentication
        args = parser.parse(loginSchema, request)
        success, token = self._authenticatePassword(args)
        if success is True:
            responseBody = {'meta': {'success': True}, 'token': token}
            response = make_response(responseBody)
            # this is hacky because I can't be bothere to write a middleware
            # to handle a bearer type authorization header
            response.headers['Authorization'] = 'Bearer ' + token
            return response
        else:
            abort(403, 'incorrect password')

    # Returns a token encoded in QR code, modified to work with BytesIO,
    # works in memory
    # https://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser
    @tokenRequired
    def get(self, token, username):
        imageIO = BytesIO()
        encodedTokenImage = qrcode.make(token)
        encodedTokenImage.save(imageIO, 'PNG')
        imageIO.seek(0)
        return send_file(imageIO, mimetype='image/png')


userView = UserResource.as_view('user')
userBP.add_url_rule('', 'UserResource', view_func=userView)
userBP.add_url_rule('/<username>/code', 'UserResource', view_func=userView)
