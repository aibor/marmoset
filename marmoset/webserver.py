from os import listdir
from flask import Flask, request, url_for
from werkzeug.exceptions import NotFound
from .flask import auth, json_app
from . import pxe


app = json_app.create('marmoset')
auth.for_all_routes(app)


@app.errorhandler(401)
def unautorized(ex):
    headers = {'WWW-Authenticate': 'Basic realm="Marmoset"'}
    return json_app.error(ex, headers=headers)


@app.route('/pxe', methods=['GET'])
def pxe_list():
    '''List all PXE entries.'''
    return json_app.response(200,
            pxe=[vars(c) for c in pxe.ClientConfig.all()])


@app.route('/pxe', methods=['POST'])
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
        return json_app.error(e, 400)
    except Exception as e:
        return json_app.error(e, 500)

    location = url_for('pxe_entry', ip_address=ip_address)
    return json_app.response(201, {'Location': location}, vars(re))


@app.route('/pxe/<ip_address>', methods=['GET'])
def pxe_show(ip_address):
    '''Lookup a PXE entry for the given ip_address.'''

    re = pxe.ClientConfig(ip_address)

    if re.exists():
        return json_app.response(200, **vars(re))
    else:
        raise NotFound


@app.route('/pxe/<ip_address>', methods=['DELETE'])
def pxe_delete(ip_address):
    '''Remove a PXE entry for the given ip_address.'''

    re = pxe.ClientConfig(ip_address)

    if re.exists():
        re.remove()
        return json_app.response(204, {}, {})
    else:
        raise NotFound


@app.route('/vm', methods=['GET'])
def vm_list():
    pass
@app.route('/vm', methods=['POST'])
def vm_create():
    pass
@app.route('/vm/<uuid>', methods=['GET'])
def vm_show():
    pass
@app.route('/vm/<uuid>', methods=['PUT'])
def vm_update():
    pass
@app.route('/vm/<uuid>', methods=['DELETE'])
def vm_delete():
    pass

