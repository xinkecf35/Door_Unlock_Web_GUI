from functools import wraps
from flask import abort, current_app, request
from json import loads
from jose.jwt import decode, JWTError


def tokenRequired(f):
    @wraps(f)
    def _validateToken(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            requestBody = loads(request.get_json())
            try:
                token = requestBody['token']
            except KeyError:
                abort(403, 'no token present')
        else:
            token = token.split()[1]
        try:
            username = request.view_args.get('username')
            if username is None:
                decode(token, current_app.config['SECRET_KEY'])
            else:
                decode(token,
                       current_app.config['SECRET_KEY'],
                       subject=username)
            kwargs['token'] = token
            return f(*args, **kwargs)
        except JWTError as err:
            abort(403, "invalid token: " + err.description)

    return _validateToken
