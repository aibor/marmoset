from flask import Blueprint, request, url_for
from werkzeug.exceptions import NotFound
from marmoset import pxe
from .flask import json


blueprint = Blueprint('pxe', __name__)


@blueprint.route('/', methods=['GET'])
def pxe_list():
    '''List all PXE entries.'''
    return json.response(200,
            pxe=[vars(c) for c in pxe.ClientConfig.all()])


@blueprint.route('/', methods=['POST'])
def pxe_create():
    '''Add a PXE entry for the given ip_address with a given password.'''
    data        = request.form
    ip_address  = data['ip_address']
    password    = data['password'] if 'password' in data else None
    label       = data['label']    if 'label' in data    else pxe.Label.names()[0]
    re          = pxe.ClientConfig(ip_address, password)
    
    try:
        re.create(pxe.Label.find(label))
    except pxe.exceptions.InputError as e:
        return json.error(e, 400)
    except Exception as e:
        return json.error(e, 500)

    location = url_for('pxe_entry', ip_address=ip_address)
    return json.response(201, {'Location': location}, vars(re))


@blueprint.route('/<ip_address>', methods=['GET'])
def pxe_show(ip_address):
    '''Lookup a PXE entry for the given ip_address.'''

    re = pxe.ClientConfig(ip_address)

    if re.exists():
        return json.response(200, **vars(re))
    else:
        raise NotFound


@blueprint.route('/<ip_address>', methods=['DELETE'])
def pxe_delete(ip_address):
    '''Remove a PXE entry for the given ip_address.'''

    re = pxe.ClientConfig(ip_address)

    if re.exists():
        re.remove()
        return json.response(204, {}, {})
    else:
        raise NotFound

