from pkg_resources import get_distribution, DistributionNotFound

from phpypam.core.api import Api as api
from phpypam.core.exceptions import PHPyPAMEntityNotFoundException

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass
