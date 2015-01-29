from flask import Flask, Response, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

__all__ = ['json_response', 'make_json_app']


def json_response(obj, code=200, headers={}):
    response = jsonify(obj)
    response.status_code = code

    for header in headers.keys():
        response.headers[header] = headers[header]

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

