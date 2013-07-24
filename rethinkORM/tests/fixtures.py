#!/usr/bin/env python
"""
Test suite for the model
"""
import rethinkdb as r
import nose.tools as nst

from rethinkORM import RethinkModel
from rethinkORM import RethinkCollection


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
    #"episodes": ["Lost City, Part 1"],
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


def setup():
    """
    Sets up the connection to RethinkDB which we'll use in the rest of the
    tests, and puts it into .repl() mode so we don't have to pass the model
    object a connection. After that, we create a new database called `model`
    and within that a table called `stargate` and sets the database to use
    `model`.
    """
    conn = r.connect('localhost', 28015)
    r.db_create("model").run(conn)
    conn.use("model")
    conn.repl()
    r.table_create("stargates").run()
    r.table_create("episodes").run()


def teardown():
    """
    Drops the whole `model` database, since it's no longer needed now that
    the tests are done.
    """
    r.db_drop("model").run()


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


def generate_docs(howMany):
    pass
