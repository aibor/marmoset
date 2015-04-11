import os
from shutil import copyfile


class Template:

    DIR = os.path.dirname(__file__) + '/../../templates'

    __instances = []

    @classmethod
    def all(cls):
        """Return all instances of the class."""
        return [x.name for x in cls.__instances]
    

    def __init__(self, name, file_name=None, callback=None):
        self.__class__.__instances.append(self)
        self.name = name
        self.file_name = name if file_name is None else file_name
        self.callback = callback


    def process(self, pxe_client_config):
        """Run the code necessary for creating a proper config."""
        if os.path.isfile(self.file_path()):
            return copyfile(self.file_path(),
                            pxe_client_config.file_path())

    def file_exists(self):
        """Return if the file exists in the template directory."""
        return (self.file_name in os.listdir(Template.DIR) and
                os.path.isfile(self.file_path()))


    def file_path(self):
        """Return complete path to the template file"""
        if self.file_name is not None:
            return Template.DIR + '/' + self.file_name

