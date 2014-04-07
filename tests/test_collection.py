#!/usr/bin/env python
"""
Test suite for the model
"""
from .fixtures import *
from rethinkORM import RethinkCollection


class baseCollection_test(object):
    def normalCollection_test(self):
        one = gateModel.create(**baseData)
        two = gateModel.create(**newData)

        record_ids = [one.id, two.id]

        collection = RethinkCollection(gateModel)

        results = collection.fetch()
        assert len(results) == 2

        result_ids = [model.id for model in results]
        for record_id in record_ids:
            assert record_id in result_ids

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


class baseCollection_filtering_test(object):
    """
    TODO: tests for:
      * Filtering
    """
    pass
