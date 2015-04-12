from flask import Flask
from flask.ext import restful
from marmoset import config
from .flask import auth
from . import pxe, vm


def run(args):
    auth.Username  = config['Webserver'].get('Username')
    auth.Password  = config['Webserver'].get('Password')

    app = Flask(config['Webserver'].get('BasicRealm'))
    auth.for_all_routes(app)
    app.config['SERVER_NAME'] = config['Webserver'].get('ServerName')

    api = restful.Api(app)

    api.add_resource(pxe.PXECollection, '/pxe')
    api.add_resource(pxe.PXEObject, '/pxe/<ip_address>')
    api.add_resource(vm.VMCollection, '/vm')
    api.add_resource(vm.VMObject, '/vm/<uuid>')
    api.add_resource(vm.VMCommand, '/vm/<uuid>/action')

    print(app.url_map)

    app.run(
        host = config['Webserver'].get('Host'),
        port = config['Webserver'].get('Port'),
        debug = config['Webserver'].getboolean('Debug')
    )

from . import subparser

