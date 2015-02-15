from flask import Flask, request, url_for
from werkzeug.exceptions import NotFound
from lib.flask_ext import *
from lib.pxe_client_config import PXEClientConfig


app = make_json_app(__name__)


@app.route('/rescue', methods=['POST'])
@requires_auth
def create_rescue_entry():
    '''Add a rescue entry for the given ip_address.'''

    ip_address = request.form['ip_address']

    re = PXEClientConfig(ip_address)

    if re.exists():
        return json_response({}, 409)

    re.create('rescue')

    location = url_for('rescue_entry', ip_address=ip_address)
    return json_response(vars(re), 201, {'Location': location})


@app.route('/rescue/<ip_address>', methods=['GET'])
@requires_auth
def rescue_entry(ip_address):
    '''Lookup a rescue entry for the given ip_address.'''

    re = PXEClientConfig(ip_address)

    if re.exists():
        return json_response(vars(re), 200)
    else:
        raise NotFound


@app.route('/rescue/<ip_address>', methods=['DELETE'])
@requires_auth
def remove_rescue_entry(ip_address):
    '''Remove a rescue entry for the given ip_address.'''

    re = PXEClientConfig(ip_address)

    if re.exists():
        re.remove()
        return json_response({}, 204)
    else:
        raise NotFound


if __name__ == "__main__":
    app.run()

