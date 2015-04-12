from .virt import Virt, connection
import xml.etree.ElementTree as ET


class Domain(Virt):

    @classmethod
    def all(cls):
       conn = connection()
       domains = conn.listAllDomains()
       conn.close()
       return [Domain(d) for d in domains]


    def __init__(self, domain):
        self.__domain = domain
        self.xml = self.get_xml()
        self.attributes = dict(
                uuid = domain.UUIDString(),
                name = self.xml.find('name').text
                )


    def get_xml(self):
        return ET.fromstring(self.__domain.XMLDesc())

