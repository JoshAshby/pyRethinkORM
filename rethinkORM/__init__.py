#!/usr/bin/env python
from rethinkModel import RethinkModel
from rethinkCollection import RethinkCollection
import tests

__version__ = '0.1.0'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ["RethinkModel",
           "RethinkCollection",
           "tests"]
