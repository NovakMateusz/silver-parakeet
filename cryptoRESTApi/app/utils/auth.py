from functools import wraps

from sanic import json, Request


def protected(wrapped):
    def decorator(function):
        wraps(function)

        async def validate_api_key(request: Request, *args, **kwargs):
            if request.app.config.API_KEY == request.headers.get('API_KEY'):
                response = await function(request, *args, **kwargs)
                return response
            return json({'status': 'Unauthorized'}, 401)

        return validate_api_key

    return decorator(wrapped)
