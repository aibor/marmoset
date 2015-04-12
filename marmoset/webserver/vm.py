from flask import Blueprint, request, url_for
from marmoset import virt
from .flask import json


blueprint = Blueprint('vm', __name__)


@blueprint.route('/', methods=['GET'])
def vm_list():
    domains = virt.Domain.all()
    return json.response(200, vm=[d.attributes for d in domains])


@blueprint.route('/', methods=['POST'])
def vm_create():
    pass


@blueprint.route('/<uuid>', methods=['GET'])
def vm_show():
    pass


@blueprint.route('/<uuid>', methods=['PUT'])
def vm_update():
    pass


@blueprint.route('/<uuid>', methods=['DELETE'])
def vm_delete():
    pass

