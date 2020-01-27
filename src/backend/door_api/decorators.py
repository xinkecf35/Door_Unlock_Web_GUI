
def handleException(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Internal Error'])
    errorResponseData = {
        'meta': {
            'success': False,
            'message': messages
        }
    }
    return errorResponseData, 500, headers


def handleBadRequest(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    errorResponseData = {
        'meta': {
            'success': False,
            'message': messages
        }
    }
    return errorResponseData, 400, headers
