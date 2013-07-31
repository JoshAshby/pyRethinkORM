#!/usr/bin/env python
"""
Test suite for the model
"""
from rethinkORM.tests.fixtures import *
from rethinkORM.rethinkCollection import RethinkCollection


class baseCollection_test(object):
    def normalCollection_test(self):
        one = gateModel.create(**baseData)
        two = gateModel.create(**newData)
        parts = [two, one]

        collection = RethinkCollection(gateModel)

        results = collection.fetch()
        assert len(results) == 2
        for model in range(len(results)):
            bit = parts[model]
            model = results[model]

            assert model.id == bit.id
            assert model.what == bit.what

        one.delete()
        two.delete()


class baseCollection_join_test(object):
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
