from .flask import auth, json
from . import pxe, vm


app = json.app('marmoset')
app.register_blueprint(pxe.blueprint, url_prefix='/pxe')
app.register_blueprint(vm.blueprint, url_prefix='/vm')

auth.for_all_routes(app)


@app.errorhandler(301)
def moved_permanently(ex):
    return json.error(ex, 301, {'location': ex.new_url})


@app.errorhandler(401)
def unautorized(ex):
    headers = {'WWW-Authenticate': 'Basic realm="Marmoset"'}
    return json.error(ex, headers=headers)

