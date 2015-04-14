from contextlib import contextmanager, closing
import libvirt
from .exceptions import Error

URI = 'qemu:///system'

@contextmanager
def connection():
    with closing(libvirt.open(URI)) as conn:
        yield conn

from . import subparser
from .domain import Domain

