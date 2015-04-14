from contextlib import contextmanager, closing
import libvirt
from .exceptions import Error
import xml.etree.ElementTree as ET


URI = 'qemu:///system'


@contextmanager
def connection():
    with closing(libvirt.open(URI)) as conn:
        yield conn

def with_unit(value):
    units = ['', 'K', 'M', 'G', 'T']
    for unit in units:
        if value < 1024 or unit == units[-1]: break
        value = value / 1024
    return "%d %sB" % (value, unit)


class Virt:

    @classmethod
    def all(cls):
        with connection() as conn:
            all = getattr(conn, cls.func['all'])()
        return [cls(i) for i in all]

    @classmethod
    def find_by(cls, attr, value):
        with connection() as conn:
            try:
                funcname = cls.func.get(attr)
                func = getattr(conn, funcname)
                return cls(func(value))
            except KeyError:
                raise Exception("attr must be 'uuid', 'id' or 'name'")
            except libvirt.libvirtError:
                return None


    def attributes(self):
        attrs = vars(self)
        del attrs['_resource']
        return attrs

    def get_xml(self, node=None):
        xml = ET.fromstring(self._resource.XMLDesc())
        return xml if node is None else xml.find(node)


class Child:

    _attrs = []
       
    def __init__(self, xml, resource):
        self._xml = xml
        self._resource = resource

    def attributes(self):
        return {attr: getattr(self, attr)() for attr in self.__class__._attrs}

from . import subparser
from .domain import Domain
from .network import Network

