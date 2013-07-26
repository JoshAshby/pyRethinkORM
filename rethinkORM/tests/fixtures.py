#!/usr/bin/env python
"""
Test suite for the model
"""
from rethinkORM import RethinkModel


"""
################################################
Test Fixtures, setup and tear down run before the first test, and after the
last test, respectfully. These are responsible for initializing the RethinkDB
connection, making a test database, and later destroying that test database.

gateModel is the test object that we'll be working with
"""
# Sample data to use as a comparison as we test the model
baseData = {
    "what": "DHD",
    "description": """Dial Home Device from the planet P3X-439, where an
    Ancient Repository of Knowledge was found, and interfaced with by Colonel
    Jack.""",
    "id": "P3X-439-DHD",
    "planet": "P3X-439",
    "episodes": 66
    }


newData = {
    "what": "Star Gate",
    "description": """Device used to form a wormhole to another gate and
    transport matter.""",
    "id": "StarGate-Earth",
    "planet": "Earth",
    "episodes": 2,
    }

classmethodData = {
    "what": "Lost City, Part 1",
    "description": """The SG1 team finds an abandoned ancient statue which
    contains an ancient knowledge head.""",
    "id": 66
    }

secondJoinData = {
    "what": "Something",
    "description": "A forgotten episode.",
    "id": 2
    }


class gateModel(RethinkModel):
    """
    Sample document object which represents the documents within the table
    `stargates`.
    """
    table = "stargates"


class episodeModel(RethinkModel):
    """Sample document object to represent episode documents within the table
    `episodes`"""
    table = "episodes"
