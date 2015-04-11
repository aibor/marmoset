from functools import wraps
from flask import request, jsonify
from werkzeug.exceptions import Unauthorized


Username = 'admin'
Password = 'APgo1VANd6YPqP0ZaJ0OK9A7WHbXzFBqe6Nz8MU9rTxKv6gIZ26nIW1cfn4GbR36'


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    global Username, Password
    print(Username, Password)
    return username == Username and password == Password


def authenticate():
    """Sends a 401 response that enables basic auth"""

    response = jsonify(message="401: Unauthorized")
    response.status_code = 401
    response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'

    return response


def required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()

        return f(*args, **kwargs)

    return decorated

