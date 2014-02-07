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


class baseCollection_orderBy_test(object):
    def orderBy_test(self):
        one = gateModel.create(**baseData)
        two = gateModel.create(**newData)

        three = episodeModel.create(**classmethodData)
        four = episodeModel.create(**secondJoinData)

        collection = RethinkCollection(gateModel)
        collection.order_by('episodes', 'asc')
        results = collection.fetch()
        assert results[0].episodes < results[1].episodes

        collection = RethinkCollection(gateModel)
        collection.order_by('episodes')
        results = collection.fetch()
        assert results[0].episodes > results[1].episodes

        one.delete()
        two.delete()
        three.delete()
        four.delete()


class baseCollection_limit_test(object):
    def limit_test(self):
        one = gateModel.create(**baseData)
        two = gateModel.create(**newData)
        three = gateModel.create(**limitData)

        collection = RethinkCollection(gateModel)
        results = collection.fetch(limit=2)
        assert len(results) == 2

        one.delete()
        two.delete()
        three.delete()


class baseCollection_offset_test(object):
    def offset_test(self):
        one = gateModel.create(**baseData)
        two = gateModel.create(**newData)
        three = gateModel.create(**limitData)

        collection = RethinkCollection(gateModel)
        collection.order_by('episodes')
        results = collection.fetch(offset=1)
        assert len(results) == 2
        assert results[0].id == three.id

        one.delete()
        two.delete()
        three.delete()


class baseCollection_limit_offset_test(object):
    def limit_offset_test(self):
        one = gateModel.create(**baseData)
        two = gateModel.create(**newData)
        three = gateModel.create(**limitData)

        collection = RethinkCollection(gateModel)
        collection.order_by('episodes')
        results = collection.fetch(limit=1, offset=2)
        assert len(results) == 1
        assert results[0].id == two.id

        one.delete()
        two.delete()
        three.delete()


class baseCollection_filtering_test(object):
    """
    TODO: tests for:
      * Filtering
    """
    pass
