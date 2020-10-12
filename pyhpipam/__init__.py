from pkg_resources import get_distribution, DistributionNotFound

from pyhpipam.core.api import Api as api
from pyhpipam.core.exceptions import PyHPIPAMEntityNotFoundException

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass
