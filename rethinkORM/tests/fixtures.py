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
