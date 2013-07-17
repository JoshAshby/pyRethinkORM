#!/usr/bin/env python
"""
Test suite for the model
"""
from rethinkORM.tests.baseSetup import *


def baseCollection_test():
    collection = RethinkCollection(gateModel)


def joinCollection_test():
    collection.joinOn(episodeModel, "episodes")
