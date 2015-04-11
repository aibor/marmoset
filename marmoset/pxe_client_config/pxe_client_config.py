import os, re
from textwrap import dedent
from string import Template as Stringtemplate
from .template import Template


__all__ = ['PXEClientConfig']


class PXEClientConfig:

    CFG_DIR = '/srv/tftp/pxelinux.cfg/'

    CFG_TEMPLATE = Stringtemplate(dedent('''\
        INCLUDE pxelinux.cfg/default
        DEFAULT instantboot
        PROMPT 0
        TIMEOUT 1
        LABEL instantboot
            KERNEL cmd.c32
            APPEND ${target_label} ${options}
        '''))

    def __init__(self, ip_address):
        if re.match('[0-9A-Z]{8}', ip_address.upper()):
            octets = [str(int(x, 16)) for x in re.findall('..', ip_address)]
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


    def create(self, template_name=None, template_args=''):
        if template_name is None:
            template_name = Template.all[0]

        content = self.__expand_template(template_name, template_args)
        self.__write_file(content)

        return self.file_path()


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

    
    def default_template(self):
        return Template.all[0]

    
    def __write_file(self, content):
        os.makedirs(PXEClientConfig.CFG_DIR, exist_ok=True)
        f = open(self.file_path(), 'w')
        f.write(content)
        f.close()


    def __expand_template(self, target_label, options):
        template = PXEClientConfig.CFG_TEMPLATE
        return template.substitute(target_label=target_label, 
                                   options=options)

