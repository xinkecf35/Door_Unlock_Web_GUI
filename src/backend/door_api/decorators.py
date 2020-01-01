from marshmallow.exceptions import ValidationError


def handleException(e):
    return e.get_response()


def handleBadRequest(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    errorResponseData = {
        'meta': {
            'success': True,
            'message': messages
        }
    }
    return errorResponseData, 400, headers
