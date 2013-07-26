#!/usr/bin/env python
"""
Test suite for the model
"""
from rethinkORM.tests.fixtures import *
from rethinkORM.rethinkCollection import RethinkCollection


class baseCollection_test(object):
    def joinCollection_test(self):
        one = gateModel.create(**baseData)
        two = gateModel.create(**newData)

        three = episodeModel.create(**classmethodData)
        four = episodeModel.create(**secondJoinData)

        collection = RethinkCollection(gateModel)
        collection.joinOn(episodeModel, "episodes")

        results = collection.fetch()
        assert len(results) == 2
        for result in results:
            assert result.episodeModel
            assert result.episodeModel.id == result.episodes

        one.delete()
        two.delete()
        three.delete()
        four.delete()
