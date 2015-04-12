from flask import Flask
from flask.ext import restful
from .flask import auth
from . import pxe, vm


app = Flask('marmoset')
app.debug = True
api = restful.Api(app)
auth.for_all_routes(app)

api.add_resource(pxe.PXECollection, '/pxe')
api.add_resource(pxe.PXEObject, '/pxe/<ip_address>')
api.add_resource(vm.VMCollection, '/vm')
api.add_resource(vm.VMObject, '/vm/<uuid>')
api.add_resource(vm.VMCommand, '/vm/<uuid>/action')
print(app.url_map)

