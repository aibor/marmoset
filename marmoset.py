from flask import Flask, Response, request, jsonify, url_for
from lib.flask.json import make_json_app
from lib.flask.auth import requires_auth
from werkzeug.exceptions import NotFound
from lib.pxe_client_config import PXEClientConfig


PXEClientConfig.DIR = '/tmp/tftpboot/pxelinux.cfg/'


app = make_json_app(__name__)


@app.route('/rescue', methods=['POST'])
@requires_auth
def create_rescue_entry():
    '''Add a rescue entry for the given ip_address.'''

    ip_address = request.form['ip_address']

    re = PXEClientConfig(ip_address)
    re.create()

    response = jsonify(vars(re))
    response.status_code = 201
    response.headers['Location'] = url_for('rescue_entry', ip_address=ip_address)

    return response


@app.route('/rescue/<ip_address>', methods=['GET'])
@requires_auth
def rescue_entry(ip_address):
    '''Lookup a rescue entry for the given ip_address.'''

    re = PXEClientConfig(ip_address)

    if re.exists():
        return jsonify(vars(re))
    else:
        raise NotFound


@app.route('/rescue/<ip_address>', methods=['DELETE'])
@requires_auth
def remove_rescue_entry(ip_address):
    '''Remove a rescue entry for the given ip_address.'''

    re = PXEClientConfig(ip_address)

    if re.exists():
        re.remove()
        response = jsonify({})
        response.status_code = 204
        return response
    else:
        raise NotFound


if __name__ == "__main__":
    app.run()

