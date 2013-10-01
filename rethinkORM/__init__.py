#!/usr/bin/env python
from rethinkModel import RethinkModel
from rethinkCollection import RethinkCollection
import tests

__version__ = '0.2.11'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ["RethinkModel",
           "RethinkCollection",
           "tests"]
