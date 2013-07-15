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
