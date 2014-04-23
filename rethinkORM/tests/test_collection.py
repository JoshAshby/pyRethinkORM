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


class baseCollection_joinAs_test(object):
    def joinCollection_test(self):
        one = gateModel.create(**baseData)
        two = gateModel.create(**newData)

        three = episodeModel.create(**classmethodData)
        four = episodeModel.create(**secondJoinData)

        collection = RethinkCollection(gateModel)
        collection.joinOnAs(episodeModel, "episodes", "epi")

        results = collection.fetch()
        assert len(results) == 2
        for result in results:
            assert result.epi
            assert result.epi.id == result.episodes

        one.delete()
        two.delete()
        three.delete()
        four.delete()


class baseCollection_orderBy_test(object):
    def orderBy_test(self):
        one = gateModel.create(**baseData)
        two = gateModel.create(**newData)

        three = episodeModel.create(**classmethodData)
        four = episodeModel.create(**secondJoinData)

        collection = RethinkCollection(gateModel)
        collection.orderBy('episodes', 'asc')
        results = collection.fetch()
        assert results[0].episodes < results[1].episodes

        collection = RethinkCollection(gateModel)
        collection.orderBy('episodes')
        results = collection.fetch()
        assert results[0].episodes > results[1].episodes

        one.delete()
        two.delete()
        three.delete()
        four.delete()


class baseCollection_offset_test(object):
    def offset_test(self):
        one = gateModel.create(**baseData)
        two = gateModel.create(**newData)
        three = gateModel.create(**newData2)

        offsetValue = 1

        collection = RethinkCollection(gateModel)
        results = collection.fetch()
        totalRows = len(results)

        collection.offset(offsetValue)
        results = collection.fetch()
        offsetRows = len(results)

        assert offsetRows == (totalRows - offsetValue)

        collection = RethinkCollection(gateModel)
        collection.orderBy('episodes').offset(offsetValue)
        results = collection.fetch()
        if len(results) > 1:
            assert results[0].episodes > results[1].episodes

        one.delete()
        two.delete()
        three.delete()


class baseCollection_limit_test(object):
    def limit_test(self):
        one = gateModel.create(**baseData)
        two = gateModel.create(**newData)
        three = gateModel.create(**newData2)

        limitValue = 2

        collection = RethinkCollection(gateModel)
        collection.limit(limitValue)
        results = collection.fetch()

        assert len(results) <= limitValue

        if limitValue > 1:
            collection = RethinkCollection(gateModel)
            collection.orderBy('episodes', 'asc').limit(limitValue)
            results = collection.fetch()
            assert results[0].episodes < results[1].episodes

            collection = RethinkCollection(gateModel)
            collection.orderBy('episodes', 'asc').offset(1).limit(limitValue)
            results = collection.fetch()
            assert results[0].episodes < results[1].episodes

        one.delete()
        two.delete()
        three.delete()


class baseCollection_filtering_test(object):
    """
    TODO: tests for:
      * Filtering
    """
    pass
