#!/usr/bin/env python
"""
Quick way to get groupings of RethinkModels objects matching the given criteria
"""
import rethinkdb as r


class RethinkCollection(object):
    """
    Base collection object providing access to groups of `RethinkModel`s
    """

    def __init__(self, model, **kwargs):
        self.table = model

    def join(self, model):
        pass

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

    def orderBy(self, field):
        pass

    def __repr(self):
        pass

    def __iter__(self):
        pass

    def __contains__(self, item):
        pass
