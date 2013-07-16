#!/usr/bin/env python
"""
Quick way to get groupings of RethinkModels objects matching the given criteria
"""
import rethinkdb as r
from rethinkModel import RethinkModel


class RethinkCollection(object):
    """
    A way to fetch groupings of documents that meet a criteria and have them
    in an iterable storage object, with each document represented by
    `RethinkModel` objects
    """
    def __init__(self, model, condition=None):
        self._documents = []
        self.model = model
        self._condititon = condition

    def join(self, model):
        pass

    def orderBy(self, field):
        pass

    def __repr(self):
        pass

    def __iter__(self):
        for doc in self._documents:
            yield doc

    # Pagination helpers...
    def paginate(self, start,finish):
        pass

    @property
    def currentPage(self):
        pass

    @property
    def perpage(self):
        pass

    @property
    def hasnextpage(self):
        pass

    @property
    def pages(self):
        pass
    # Okay, enough pagination

    def fetch(self):
        pass
