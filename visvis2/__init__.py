__version__ = "0.1.0"
version_info = tuple(map(int, __version__.split(".")))

from ._functions import *  # noqa
from ._view import View  # noqa
