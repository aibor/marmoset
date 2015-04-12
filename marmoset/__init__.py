import configparser
from . import pxe, virt

config = configparser.ConfigParser()

config['Webserver'] = dict(
    Username    = 'admin',
    Password    = 'secret',
    BasicRealm  = __name__,
)

config['PXEConfig'] = dict(
    ConfigDirectory = '/srv/tftp/pxelinux.cfg'
)

config['PXELabel']  = dict(
)

config['Libvirt']   = dict(
    URI = 'qemu:///system'
)


config.read('marmoset.conf')


if config.options('PXELabel').__len__() == 0:
    raise Exception('No PXELabel defined in config')
else:
    # Create pxe label list.
    [pxe.Label(n, cb) for n, cb in config['PXELabel'].items()]

pxe.ClientConfig.CFG_DIR    = config['PXEConfig'].get('ConfigDirectory')
virt.URI                    = config['Libvirt'].get('URI')

