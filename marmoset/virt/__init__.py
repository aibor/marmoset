from contextlib import contextmanager, closing
from os import path
import libvirt
from .exceptions import Error
import xml.etree.ElementTree as ET


URI = 'qemu:///system'


@contextmanager
def connection():
    """
    Return a contextmanager for a libvirt connection.
    """
    with closing(libvirt.open(URI)) as conn:
        yield conn

def with_unit(value):
    """
    Return a string of the converted numerical @value with the proper
    unit name.
    """
    units = ['', 'Ki', 'Mi', 'Gi', 'Ti']
    for unit in units:
        if value < 1024 or unit == units[-1]: break
        value = value / 1024
    return "%d %sB" % (value, unit)


class Virt:

    func = {}

    TEMPLATE_DIR = path.join(path.dirname(__file__), 'templates')

    @classmethod
    def all(cls):
        """
        Return a list with all instances. In order to work, the
        resource must provide the class variable 'func', which has to
        be a dict with at least the key 'all' and the the name of the
        libvirt function to call as value.
        """
        with connection() as conn:
            all = getattr(conn, cls.func['all'])()
        return [cls(i) for i in all]

    @classmethod
    def find_by(cls, attr, value):
        """"
        Return a class instance identified by id, uuid or name.
        
        @attr: identifier attribute
        @value: value to search for
        
        In order to work, the resource must provide the class variable
        'func', which has to be a dict with at least the keys id, uuid
        and name and the respective libvirt function name to call as
        values.
        """
        with connection() as conn:
            try:
                funcname = cls.func[attr]
                func = getattr(conn, funcname)
                return cls(func(value))
            except KeyError:
                message = "dynamic finder method for attr '%s' not implemented"
                raise Exception(message % attr)
            except libvirt.libvirtError:
                return None


    def attributes(self, **kw):
        """
        Set and get attributes of the resource. Items in @kw with empty
        or None values will be dropped.
        """
        vars(self).update({k: v for k, v in kw.items() if v})
        return {k: v for k, v in vars(self).items() if k != '_resource'}

    def get_xml(self, node=None):
        """
        Return the XML description of the libvirt instance. If @node is
        given, only the child node is returned instead of the root node.
        """
        xml = ET.fromstring(self._resource.XMLDesc())
        return xml if node is None else xml.find(node)

    def template_file(self):
        return path.join(self.__class__.TEMPLATE_DIR,
                         self.__class__.__name__.lower() + '.xml')



class Child:

    _attrs = []
       
    def __init__(self, xml, resource):
        """
        @xml: Libvirt XML Description of the resource part
        @resource: Libvirt object of the parent resource
        """
        self._xml = xml
        self._resource = resource

    def attributes(self):
        return {a: getattr(self, a)() for a in self.__class__._attrs}

from . import subparser
from .domain import Domain
from .network import Network

