from os import listdir
from flask import Flask, request, url_for
from werkzeug.exceptions import NotFound
from .flask import auth, json_app
from . import pxe


app = json_app.create('marmoset')


@app.route('/pxe', methods=['GET'])
@auth.required
def pxe_entries():
    '''List all PXE entries.'''

    entries = [vars(c) for c in pxe.ClientConfig.all()]
    return json_app.response({'entries': entries}, 200)


@app.route('/pxe', methods=['POST'])
@auth.required
def create_pxe_entry():
    '''Add a PXE entry for the given ip_address with a given password.'''

    data = request.form

    ip_address  = data['ip_address']
    password    = data['password'] if 'password' in data else None
    label       = data['label']    if 'label' in data    else pxe.Label.names()[0]

    re = pxe.ClientConfig(ip_address, password)
    
    try:
        re.create(pxe.Label.find(label))
    except Exception as e:
        return json_app.response({'message': str(e)}, 400)

    location = url_for('pxe_entry', ip_address=ip_address)
    return json_app.response(vars(re), 201, {'Location': location})


@app.route('/pxe/<ip_address>', methods=['GET'])
@auth.required
def pxe_entry(ip_address):
    '''Lookup a PXE entry for the given ip_address.'''

    re = pxe.ClientConfig(ip_address)

    if re.exists():
        return json_app.response(vars(re), 200)
    else:
        raise NotFound


@app.route('/pxe/<ip_address>', methods=['DELETE'])
@auth.required
def remove_pxe_entry(ip_address):
    '''Remove a PXE entry for the given ip_address.'''

    re = pxe.ClientConfig(ip_address)

    if re.exists():
        re.remove()
        return json_app.response({}, 204)
    else:
        raise NotFound

