from . import connection, Parent, Child


class Network(Parent):
    _func = dict(
        all     = 'listAllNetworks',
        uuid    = 'networkLookupByUUIDString',
        id      = 'networkLookupByID',
        name    = 'networkLookupByName'
    )

    @property
    def uuid(self):
        return self._resource.UUIDString()

    @property
    def name(self):
        return self._resource.name()

    @property
    def bridge(self):
        return self._resource.bridgeName()

    @property
    def hosts(self):
        hosts = self.get_xml().findall('.//host')
        return [Network.Host(host, self._resource) for host in hosts]


    class Host(Child):
        @property
        def mac_address(self):
            return self._xml.attrib.get('mac_address')

        @property
        def name(self):
            return self._xml.attrib.get('name')

        @property
        def ip_address(self):
            return self._xml.attrib.get('ip_address')

