from . import connection, Virt, Child


class Network(Virt):
    func = dict(
        all     = 'listAllNetworks',
        uuid    = 'networkLookupByUUIDString',
        id      = 'networkLookupByID',
        name    = 'networkLookupByName'
    )

    def __init__(self, network=None):
        self._resource = network
        if network:
            self.uuid       = network.UUIDString()
            self.name       = network.name()
            self.hosts      = [h.attributes() for h in self.hosts()]

    def bridge(self):
        return self._resource.bridgeName()

    def hosts(self):
        hosts = self.get_xml().findall('.//host')
        return [Network.Host(host, self._resource) for host in hosts]


    class Host(Child):

        _attrs = ['mac_address', 'name', 'ip_address']

        def mac_address(self):
            return self._xml.attrib.get('mac_address')

        def name(self):
            return self._xml.attrib.get('name')

        def ip_address(self):
            return self._xml.attrib.get('ip_address')

