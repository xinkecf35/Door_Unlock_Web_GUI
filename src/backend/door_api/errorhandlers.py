
def handleException(err):
    response = getattr(err, "response", None)
    if response:
        return response
    errorResponseData = {
        'meta': {
            'success': False,
            'description': err.description,
            'messages': []
        }
    }
    return errorResponseData, 500


def handleBadRequest(err):
    response = getattr(err, "response")
    if response:
        return response
    data = getattr(err, 'data', None)
    messages = []
    if data:
        messages = data['messages']
    errorResponseData = {
        'meta': {
            'success': False,
            'description': err.description,
            'message': messages
        }
    }
    return errorResponseData, 400


def handleForbiddenRequest(err):
    response = getattr(err, 'response')
    if response:
        return response
    e = getattr(err, 'exc', None)
    description = err.description
    messages = []
    if e:
        messages = e.message
        description = e.description
    errorResponseData = {
        'meta': {
            'success': False,
            'description': description,
            'message': messages
        }
    }
    return errorResponseData, 403
