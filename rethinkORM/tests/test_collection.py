#!/usr/bin/env python
"""
Test suite for the model
"""
from rethinkORM.tests.fixtures import *


def baseCollection_test():
    generate_docs(10)
    collection = RethinkCollection(gateModel)
    assert len(collection) == 10


def joinCollection_test():
    collection.join(episodeModel, "episode_id", "Episode")

    results = collection.fetch()
    for result in results:
        assert result.Episode.id == result.episode_id
