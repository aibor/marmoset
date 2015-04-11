from functools import wraps
from flask import Flask, Response, request, jsonify
from werkzeug.exceptions import default_exceptions, HTTPException, Unauthorized
try:
    import settings
except: pass


if 'settings' in globals() and 'USERNAME' in vars(settings):
    USERNAME = settings.USERNAME
else:
    USERNAME = 'admin'

    
if 'settings' in globals() and 'PASSWORD' in vars(settings):
    PASSWORD = settings.PASSWORD
else:
    PASSWORD = 'secret'


__all__ = ['json_response', 'make_json_app', 'requires_auth']


def json_response(obj, code=200, headers={}):
    response = jsonify(obj)
    response.status_code = code
    response.headers.extend(headers)

    return response


def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        code = ex.code if isinstance(ex, HTTPException) else 500
        return json_response({'message': str(ex)}, code)

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.keys():
        app.error_handler_spec[None][code] = make_json_error

    return app


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == USERNAME and password == PASSWORD


def authenticate():
    """Sends a 401 response that enables basic auth"""

    response = jsonify(message="401: Unauthorized")
    response.status_code = 401
    response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'

    return response


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()

        return f(*args, **kwargs)

    return decorated

