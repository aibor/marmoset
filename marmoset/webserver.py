from os import listdir
from flask import Flask, request, url_for
from werkzeug.exceptions import NotFound
from .flask.extensions import *
from . import pxe


webserver = make_json_app('marmoset')


@webserver.route('/pxe', methods=['POST'])
@requires_auth
def create_pxe_entry():
    '''Add a PXE entry for the given ip_address with a given password.'''

    data = request.form

    ip_address  = data['ip_address']
    password    = data['password'] if 'password' in data else None
    label       = data['label']    if 'label' in data    else pxe.Label[0].name

    re = pxe.ClientConfig(ip_address, password)
    
    try:
        efile, password = re.create(pxe.Label.find(args.label))
    except e:
        return json_response({'message': str(e)}, 400)

    location = url_for('pxe_entry', ip_address=ip_address)
    return json_response(vars(re), 201, {'Location': location})


@webserver.route('/pxe/<ip_address>', methods=['GET'])
@requires_auth
def pxe_entry(ip_address):
    '''Lookup a PXE entry for the given ip_address.'''

    re = pxe.ClientConfig(ip_address)

    if re.exists():
        return json_response(vars(re), 200)
    else:
        raise NotFound


@webserver.route('/pxe/<ip_address>', methods=['DELETE'])
@requires_auth
def remove_pxe_entry(ip_address):
    '''Remove a PXE entry for the given ip_address.'''

    re = pxe.ClientConfig(ip_address)

    if re.exists():
        re.remove()
        return json_response({}, 204)
    else:
        raise NotFound

