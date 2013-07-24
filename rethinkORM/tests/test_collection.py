#!/usr/bin/env python
"""
Test suite for the model
"""
from rethinkORM.tests.fixtures import *
from rethinkORM.rethinkCollection import RethinkCollection


#def baseCollection_test():
    #generate_docs(10)
    #collection = RethinkCollection(gateModel)
    #assert len(collection) == 10


def joinCollection_test():
    gateModel.create(**baseData)
    gateModel.create(**newData)

    episodeModel.create(**classmethodData)
    episodeModel.create(**secondJoinData)

    collection = RethinkCollection(gateModel)
    collection.joinOn(episodeModel, "episodes")

    results = collection.fetch()
    for result in results:
        assert result.Episode.id == result.episodes
