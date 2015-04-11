import os, re, crypt, base64
from textwrap import dedent
from string import Template as Stringtemplate


__all__ = ['PXELabel', 'PXEClientConfig']


class PXELabel:
    class Exception(Exception):

        def __init__(self, msg):
            self.msg = msg

        def __str__(self):
            return self.msg


    __instances = []


    @classmethod
    def find(cls, name):
        for i in cls.__instances:
            if name == i.name:
                return i
        raise Exception("No PXELabel with name '%s' found." % (name,))


    @classmethod
    def names(cls):
        """Return the names of all instances of the class."""
        return [x.name for x in cls.__instances]


    def __init__(self, name, callback=None):
        if callback in (None, ''):
            callback=None
        elif not PXEClientConfig.has_callback(callback):
            msg = "Callback method '%s' doesn't exist. Available: %s"
            callbacklist = ', '.join(PXEClientConfig.callbacks())
            raise Exception(msg % (callback, callbacklist))

        self.__class__.__instances.append(self)
        self.name = name
        self.callback = callback


class PXEClientConfig:

    CFG_DIR = '/srv/tftp/pxelinux.cfg/'

    CFG_TEMPLATE = Stringtemplate(dedent('''\
        INCLUDE pxelinux.cfg/default
        DEFAULT instantboot
        PROMPT 0
        TIMEOUT 1
        LABEL instantboot
            KERNEL cmd.c32
            APPEND ${label} ${options}
        '''))


    @classmethod
    def all(cls):
        entries = []
        for entry_file in os.listdir(PXEClientConfig.CFG_DIR):
            if re.match('[0-9A-Z]{8}', entry_file):
                entries.append(PXEClientConfig(entry_file))
        return entries


    @classmethod
    def has_callback(cls, name):
        return name in cls.callbacks()


    @classmethod
    def callbacks(cls):
        cbs = []
        for m in dir(cls):
            if m[:3] == 'cb_':
                cbs.append(m[3:])
        return cbs

    def __init__(self, ip_address, password=None):
        if re.match('[0-9A-Z]{8}', ip_address.upper()):
            octets = [str(int(x, 16)) for x in re.findall('..', ip_address)]
            ip_address = '.'.join(octets)

        self.ip_address = ip_address

        if not password in [None, '']:
            self.password = password


    def exists(self):
        return os.path.isfile(self.file_path())


    def create(self, label):
        pxe_label = PXELabel.find(label)

        if pxe_label.callback is None:
            options = None
        else:
            func = getattr(self, 'cb_%s' % pxe_label.callback)
            options = func()

        content = self.__expand_template(label, options)
        self.__write_config_file(content)


    def remove(self):
        if self.exists():
            os.remove(self.file_path())
            return True
        else:
            return False


    def file_name(self):
        octets = map(int, self.ip_address.split('.'))
        return "%02X%02X%02X%02X" % tuple(octets)


    def file_path(self, name=None):
        if name is None:
            name = self.file_name()

        cfgdir = PXEClientConfig.CFG_DIR.rstrip('/')
        return cfgdir + '/' + name

    
    def __write_config_file(self, content, path=None):
        if path is None:
            path = self.file_path()

        os.makedirs(PXEClientConfig.CFG_DIR, exist_ok=True)
        f = open(path, 'w')
        f.write(content)
        f.close()


    def __expand_template(self, label, options = None):
        if options is None:
            options = ''
        template = PXEClientConfig.CFG_TEMPLATE
        return template.substitute(label=label, 
                                   options=options)


    def __mkpwhash(self):
        if 'password' not in vars(self) or self.password in [None, '']:
            pw = base64.b64encode(os.urandom(16), b'-_')[:16]
            self.password = pw.decode('utf-8')
        return crypt.crypt(self.password, self.__mksalt())


    def __mksalt(self):
        return crypt.mksalt(crypt.METHOD_SHA512)


    def cb_setpwhash(self):
        return 'HASH=' + self.__mkpwhash()


    def cb_createpwhashfile(self):
        file_path = self.file_path('PWHASH.' + self.ip_address)
        self.__write_config_file(self.__mkpwhash(), file_path)
        return None

