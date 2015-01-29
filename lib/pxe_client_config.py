import os

__all__ = ['PXEClientConfig']


class PXEClientConfig:

    DIR = '/tftpboot/pxelinux.cfg/'

    def __init__(self, ip_address):
        self.ip_address = ip_address

    def exists(self):
        return os.path.isfile(self.file_path())

    def create(self):
        os.makedirs(PXEClientConfig.DIR, exist_ok=True)
        f = open(self.file_path(), 'w+')
        f.write("INCLUDE pxelinux.cfg/default\n"
                "DEFAULT rescue\n"
                "PROMPT 0\n"
                "TIMEOUT 1\n")
        f.close()

    def remove(self):
        os.remove(self.file_path())

    def file_name(self):
        octets = map(int, self.ip_address.split('.'))
        return "%02X%02X%02X%02X" % tuple(octets)

    def file_path(self):
        cfgdir = PXEClientConfig.DIR.rstrip('/')
        return cfgdir + '/' + self.file_name()

