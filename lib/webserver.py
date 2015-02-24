from os import listdir
from flask import Flask, request, url_for
from werkzeug.exceptions import NotFound
from .flask_ext import *
from .pxe_client_config import PXEClientConfig


webserver = make_json_app('marmoset')


@webserver.route('/pxe', methods=['POST'])
@requires_auth
def create_pxe_entry():
    '''Add a PXE entry for the given ip_address.'''

    ip_address = request.form['ip_address']

    if 'template' in request.form:
        template = request.form['template']
    else:
        template = 'rescue'

    re = PXEClientConfig(ip_address)

    if re.exists():
        return json_response({}, 409)

    try:
        re.create(template)
    except FileNotFoundError:
        return json_response(
                {'message': 'Template not found: ' +
                    template +
                    '. Available templates: ' +
                    ', '.join(listdir(PXEClientConfig.TMPL_DIR)) },
                400
                )


    location = url_for('pxe_entry', ip_address=ip_address)
    return json_response(vars(re), 201, {'Location': location})


@webserver.route('/pxe/<ip_address>', methods=['GET'])
@requires_auth
def pxe_entry(ip_address):
    '''Lookup a PXE entry for the given ip_address.'''

    re = PXEClientConfig(ip_address)

    if re.exists():
        return json_response(vars(re), 200)
    else:
        raise NotFound


@webserver.route('/pxe/<ip_address>', methods=['DELETE'])
@requires_auth
def remove_pxe_entry(ip_address):
    '''Remove a PXE entry for the given ip_address.'''

    re = PXEClientConfig(ip_address)

    if re.exists():
        re.remove()
        return json_response({}, 204)
    else:
        raise NotFound

