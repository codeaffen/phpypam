"""Package that provides phpIPAM API interface."""
import importlib.metadata

from phpypam.core.api import Api as api
from phpypam.core.exceptions import PHPyPAMEntityNotFoundException

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:

    pass
