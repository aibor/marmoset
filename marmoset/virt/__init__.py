from contextlib import contextmanager, closing
import libvirt
from .exceptions import Error
from . import subparser

URI = 'qemu:///system'

@contextmanager
def connection():
    with closing(libvirt.open(URI)) as conn:
        yield conn

