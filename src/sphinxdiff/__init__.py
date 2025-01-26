"""Sphinx extension for a diff view of two documents"""

from .diff import setup as diff_setup
from . import prototype


__version__ = '0.0.2'
__version_full__ = __version__




diff = prototype.diff


def setup(app):
    """Initialization point of the sphinx extension."""

    diff_setup(app)
    return {'version': __version__,
            }

