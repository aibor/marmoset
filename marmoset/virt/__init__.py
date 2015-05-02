from .domain import Domain
from .network import Network
from .storage import Storage
from pprint import pprint


def create(args):
    network = Network.find_by('name', Network.DEFAULT)
    if network.knows_ip_address(args['ip_address']):
        raise Exception('IP address already assigned')

    name = "{}_{}".format(args['user'], args['name'])
    storage = Storage.find_by('name', Storage.DEFAULT)
    disk = storage.create_volume(name, args['disk'])

    domain = Domain.create(
        name = args['name'],
        user = args['user'],
        memory = base.parse_unit(args['memory'])[0],
        unit = base.parse_unit(args['memory'])[1],
        vcpu = args['cpu'],
        disks = [dict(path = disk.path, bus = 'virtio', target = 'hda')],
        interfaces = [dict(model = 'virtio', network = Network.DEFAULT)])

    network.add_host(
        domain.interfaces[0].mac_address,
        args['ip_address'],
        name)

    return domain


def list(args):
    for domain in Domain.all():
        pprint(domain.attributes())


def edit(args):
    domain = Domain.find_by('uuid', args['uuid'])


def remove(args):
    domain = Domain.find_by('uuid', args['uuid'])
    try: domain.shutdown()
    except: pass
    for interface in domain.interfaces:
        host = interface.host()
        if not host is None:
            host.delete()
    if domain.undefine():
        print('Removed', domain.name())

