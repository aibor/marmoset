from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions, HTTPException


def response(obj, code=200, headers={}):
    response = jsonify(obj)
    response.status_code = code
    response.headers.extend(headers)

    return response


def create(import_name, **kwargs):
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

