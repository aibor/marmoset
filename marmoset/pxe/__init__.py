from .label import Label
from .client_config import ClientConfig

def create(config, args):
    pxe_client = ClientConfig(args.ip_address, args.password)
    pxe_client.create(Label.find(args.label))
    msg = 'Created %s with password %s' 
    print(msg % (pxe_client.file_path(), pxe_client.password))


def list(config, args):
    for pxe_client in ClientConfig.all():
        print('%s: %s' % (pxe_client.ip_address, pxe_client.label))


def remove(config, args):
    pxe_client = ClientConfig(args.ip_address)
    if pxe_client.remove():
        print('Removed', pxe_client.file_path())
    else:
        print('No entry found for', pxe_client.ip_address)

