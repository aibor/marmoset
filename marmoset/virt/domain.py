from .exceptions import Error
from .network import Network
from . import connection, with_unit, domain_states, Virt, Child
from libvirt import libvirtError
from string import Template


class Domain(Virt):

    func = dict(
        all     = 'listAllDomains',
        uuid    = 'lookupByUUIDString',
        id      = 'lookupByID',
        name    = 'lookupByName'
    )

    def __init__(self, domain=None):
        self._resource = domain
        if domain:
            self.uuid       = domain.UUIDString()
            self.name       = domain.name()
            self.memory     = self.memory()
            self.vcpu       = self.vcpu()
            self.state      = self.state()
            self.disks      = [d.attributes() for d in self.disks()]
            self.interfaces = [i.attributes() for i in self.interfaces()]

    def memory(self):
        return with_unit(int(self.get_xml('memory').text)*1024)

    def vcpu(self):
        return self.get_xml('vcpu').text

    def get_info(self):
        keys = ['state', 'memory_max', 'memory', 'vcpu', 'cpu_time']
        info = dict(zip(keys, self._resource.info()))

    def state(self):
        state_id, reason_id = self._resource.state()
        state   = domain_states.States[state_id]
        reason  = domain_states.Reasons[state][reason_id]
        return dict(state=state, reason=reason)

    def disks(self):
        disks = self.get_xml('devices').findall('disk')
        return [Domain.Disk(disk, self._resource) for disk in disks]

    def interfaces(self):
        interfaces = self.get_xml('devices').findall('interface')
        return [Domain.Interface(iface, self._resource) for iface in interfaces]

    def start(self):
        self._command('create')

    def stop(self):
        self._command('destroy')

    def shutdown(self):
        self._command('shutdown')

    def reset(self):
        self._command('reset')

    def undefine(self):
        self._command('undefine')
        self._resource = None

    def save(self):
        if not self._resource:
            with open(self.template_file()) as f:
                template = Template(f.read())
            xml = template.substitute(self.attributes())
            with connection() as conn:
                self._resource = conn.defineXML(xml)


    def _command(self, cmd, *args, **kwargs):
        try:
            func = getattr(self._resource, cmd)
            return func(*args, **kwargs)
        except libvirtError as e:
            raise Error(str(e))


    class Disk(Child):
        _attrs = ['path', 'target', 'type', 'bus', 'capacity']

        def path(self):
            source = self._xml.find('source')
            return list(source.attrib.values())[0]

        def target(self):
            return self._xml.find('target').attrib['dev']

        def type(self):
            return self._xml.attrib['device']

        def bus(self):
            return self._xml.find('target').attrib['bus']

        def blockinfo(self):
            keys    = ['capacity', 'allocation', 'physical']
            values  = self._resource.blockInfo(self.target())
            return dict(zip(keys, values))

        def capacity(self):
            value = self.blockinfo()['capacity']
            return with_unit(value)


    class Interface(Child):

        _attrs = ['mac_address', 'model', 'ip_address']

        def type(self):
            return self._xml.attrib['type']

        def mac_address(self):
            return self._xml.find('mac').attrib['address']

        def model(self):
            return self._xml.find('model').attrib['type']

        def network(self):
            source = self._xml.find('source')
            return source.attrib['network'] if source else None

        def host(self):
            if not self.network(): return
            network = Network.find_by('name', self.network())
            if not network: return
            for host in network.hosts():
                if host.mac_address() == self.mac_address():
                    return host

        def ip_address(self):
            host = self.host()
            if host:
                return host.ip_address()
            

