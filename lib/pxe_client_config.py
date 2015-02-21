import os, re
from shutil import copyfile


__all__ = ['PXEClientConfig']


class PXEClientConfig:

    CFG_DIR = '/srv/tftp/pxelinux.cfg/'

    TMPL_DIR = os.path.dirname(__file__) + '/../templates'


    def __init__(self, ip_address):
        if re.match('[0-9A-Z]{8}', ip_address.upper()):
            octets = [ str(int(x, 16)) for x in re.findall('..', ip_address) ]
            ip_address = '.'.join(octets)

        self.ip_address = ip_address


    @classmethod
    def all(cls):
        entries = []
        for entry_file in os.listdir(PXEClientConfig.CFG_DIR):
            if re.match('[0-9A-Z]{8}', entry_file):
                entries.append(PXEClientConfig(entry_file))
        return entries


    def exists(self):
        return os.path.isfile(self.file_path())


    def create(self, pxe_file = 'rescue'):
        os.makedirs(PXEClientConfig.CFG_DIR, exist_ok=True)
        return copyfile(PXEClientConfig.TMPL_DIR + '/' + pxe_file,
                self.file_path())


    def remove(self):
        if self.exists():
            os.remove(self.file_path())
            return True
        else:
            return False


    def file_name(self):
        octets = map(int, self.ip_address.split('.'))
        return "%02X%02X%02X%02X" % tuple(octets)


    def file_path(self):
        cfgdir = PXEClientConfig.CFG_DIR.rstrip('/')
        return cfgdir + '/' + self.file_name()

