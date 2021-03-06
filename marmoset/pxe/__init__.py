from .label import Label
from .client_config import ClientConfig


def create(args):
    pxe_client = ClientConfig(args.ip_address, args.password, args.script)
    used_options = pxe_client.create(Label.find(args.label))

    msg = 'Created %s with following Options: %s'

    print(msg % (pxe_client.file_path(), " ".join(used_options)))

def list(args):
    for pxe_client in ClientConfig.all():
        print('%s: %s' % (pxe_client.ip_address, pxe_client.label))


def remove(args):
    pxe_client = ClientConfig(args.ip_address)
    if pxe_client.remove():
        print('Removed', pxe_client.file_path())
    else:
        print('No entry found for', pxe_client.ip_address)

