from flask import Response, jsonify


class JSONResponse(Response):
    default_mimetype = 'application/json'
    default_status = 200
    charset = 'utf-8'

    def __init__(
        self,
        response=None,
        status=None,
        headers=None,
        mimetype=None,
        content_type=None,
        direct_passthrough=False
    ):
        pass

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            if 'meta' not in rv:
                rv['meta'] = {'success': True}
            rv = jsonify(rv)
        return super(JSONResponse, cls).force_type(rv, environ)
