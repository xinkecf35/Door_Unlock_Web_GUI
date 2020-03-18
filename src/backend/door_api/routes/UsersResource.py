from flask import Blueprint, abort
from flask.views import MethodView
from webargs.flaskparser import use_args

from door_api.extensions import db
from door_api.models.UserSchema import UserSchema

usersBP = Blueprint('users', __name__, url_prefix='/users')
excludeFields = ['password', 'admin']
dumpSchema = UserSchema(exclude=excludeFields)


class UsersResource(MethodView):
    # TODO: Make authnentication required here
    # Creates a User
    @use_args(UserSchema(), location='json')
    def post(self, newUser):
        try:
            db.session.add(newUser)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)
        user = dumpSchema.dump(newUser)
        return {'meta': {'success': True}, 'user': user}, 201

    # Creates multiple users
    @use_args(UserSchema(many=True), location='json')
    def put(self, newUsers):
        try:
            for user in newUsers:
                db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)
        manySchemaDump = UserSchema(many=True, exclude=excludeFields)
        dumpedUsers = manySchemaDump.dump(newUsers)
        responseData = {
            'meta': {
                'success': True,
                'message': ['all users added']
            },
            'users': dumpedUsers
        }
        return responseData, 201


usersBP.add_url_rule('',
                     'UsersResource',
                     view_func=UsersResource.as_view('users'))
