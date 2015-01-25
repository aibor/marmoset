from flask import Flask, Response, request, jsonify
from jsonflask import make_json_app
from flaskauth import requires_auth
from werkzeug.exceptions import NotFound
from rescue_entry import RescueEntry

app = make_json_app(__name__)

RescueEntry.PXECFG_DIR = '/tmp/tftpboot/pxelinux.cfg/'

@app.route('/rescue', methods=['POST'])
@requires_auth
def create_rescue_entry():
    '''Add a rescue entry for the given ip_address.'''
    re = RescueEntry(request.form['ip_address'])
    re.create()
    return jsonify(vars(re))

@app.route('/rescue/<ip_address>', methods=['GET'])
@requires_auth
def rescue_entry(ip_address):
    '''Lookup a rescue entry for the given ip_address.'''
    re = RescueEntry(ip_address)
    if re.exists():
        return jsonify(vars(re))
    else:
        raise NotFound

@app.route('/rescue/<ip_address>', methods=['DELETE'])
@requires_auth
def remove_rescue_entry(ip_address):
    '''Remove a rescue entry for the given ip_address.'''
    re = RescueEntry(ip_address)
    if re.exists():
        re.remove()
        return Response('', 204)
    else:
        raise NotFound

if __name__ == "__main__":
    app.run()

