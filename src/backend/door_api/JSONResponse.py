from flask import Response, jsonify


class JSONResponse(Response):
    default_mimetype = 'application/json'
    default_status = 200
    charset = 'utf-8'

    def __init__(self,
                 response=None,
                 status=None,
                 headers=None,
                 mimetype=None,
                 content_type=None,
                 direct_passthrough=False):
        super(Response, self).__init__(response=response,
                                       status=status,
                                       headers=headers,
                                       mimetype=mimetype,
                                       content_type=content_type,
                                       direct_passthrough=direct_passthrough)

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(Response, cls).force_type(rv, environ)
