from .virt import Virt, connection
from .exceptions import Error
from . import domain_states
import xml.etree.ElementTree as ET
from libvirt import libvirtError


class Domain(Virt):

    class Disk:

        def __init__(self, xml, domain):
            self.__xml = xml
            self.__domain = domain

        def attributes(self):
            return dict(
                    path        = self.path(),
                    target      = self.target(),
                    type        = self.type(),
                    bus         = self.bus(),
                    capacity_GB = self.blockinfo()['capacity'] >> 30
                    )

        def path(self):
            source = self.__xml.find('source')
            return list(source.attrib.values())[0]

        def target(self):
            return self.__xml.find('target').attrib['dev']

        def type(self):
            return self.__xml.attrib['device']

        def bus(self):
            return self.__xml.find('target').attrib['bus']

        def blockinfo(self):
            keys    = ['capacity', 'allocation', 'physical']
            values  = self.__domain.blockInfo(self.target())
            return dict(zip(keys, values))


    @classmethod
    def all(cls):
        with connection() as conn:
            domains = conn.listAllDomains()
        return [Domain(d) for d in domains]

    @classmethod
    def find(cls, uuid):
        with connection() as conn:
            try:
                domain = conn.lookupByUUIDString(uuid)
                domain = Domain(domain)
            except libvirtError:
                domain = None
        return domain


    def __init__(self, domain):
        self.__domain = domain
        self.attributes = self.get_info()
        del self.attributes['cpu_time']
        self.attributes.update(dict(
            uuid    = domain.UUIDString(),
            name    = domain.name(),
            state   = self.state(),
            disks   = [d.attributes() for d in self.disks()]
            ))

    def get_xml(self, node=None):
        xml = ET.fromstring(self.__domain.XMLDesc())
        return xml if node is None else xml.find(node)


    def get_info(self):
        keys = ['state', 'memory_max', 'memory', 'vcpu', 'cpu_time']
        return dict(zip(keys, self.__domain.info()))

    def state(self):
        state_id, reason_id = self.__domain.state()
        state   = domain_states.States[state_id]
        reason  = domain_states.Reasons[state][reason_id]
        return dict(state=state, reason=reason)

    def disks(self):
        disks = self.get_xml('devices').findall('disk')
        return [Domain.Disk(disk, self.__domain) for disk in disks]

    def start(self):
        self.__command('create')

    def stop(self):
        self.__command('destroy')

    def shutdown(self):
        self.__command('shutdown')

    def reset(self):
        self.__command('reset')

    def __command(self, cmd, *args, **kwargs):
        try:
            getattr(self.__domain, cmd)(*args, **kwargs)
        except libvirtError as e:
            raise Error(str(e))

