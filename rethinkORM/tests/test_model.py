#!/usr/bin/env python
"""
Test suite for the model
"""
import rethinkdb as r
import nose.tools as nst

from rethinkORM import RethinkModel


"""
################################################
Test Fixtures, setup and teardown run before the first test, and after the last
test, respectfully. These are responsable for initializing the RethinkDB
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
    r.table_create("stargate").run()


def teardown():
    """
    Drops the whole `model` database, since it's no longer needed now that
    the tests are done.
    """
    r.db_drop("model").run()


class gateModel(RethinkModel):
    """
    Sample document object which represents the documents within the table
    `stargate`.
    """
    _table = "stargate"


"""
################################################
Start Unittests
"""


# Sample data to use as a comparison as we test the model
data = {
    "what": "DHD",
    "description": """Dial Home Device from the planel P3X-439, where an
    Ancient Repository of Knowledge was found, and interfaced with by Colonel
    Jack.""",
    "id": "P3X-439-DHD",
    "planet": "P3X-439",
    "episodes": ["Lost City, Part 1"],
    }


def insert_test():
    """
    Creates a new object, and inserts it, using `.save()`
    """
    dhdProp = gateModel(what="DHD", description="Dial Home Device",
                        planet=data["planet"],
                        id=data["id"])
    assert dhdProp.save()
    del dhdProp


def load_insert_test():
    """
    Loads the previously inserted document, and checks all the fields to
    ensure everything got stored as we expected.
    """
    dhdProp = gateModel.load(data["id"])
    assert dhdProp.id == data["id"]
    assert dhdProp.what == "DHD"
    assert dhdProp.planet == data["planet"]
    del dhdProp


def modify_test():
    """
    Next, we get the object again, and this time, we modify it, and save it.
    """
    dhdProp = gateModel(id=data["id"])
    dhdProp.what = data["what"]
    dhdProp.description = data["description"]
    dhdProp.episodes = data["episodes"]
    assert dhdProp.save()
    del dhdProp


def load_modify_test():
    """
    Like the insert_test, we go through, load the modified document and
    check the fields to ensure everything is correct.
    """
    dhdProp = gateModel.load(data["id"])
    assert dhdProp.id == data["id"]
    assert dhdProp.what == data["what"]
    assert dhdProp.planet == data["planet"]
    assert dhdProp.episodes == data["episodes"]
    assert dhdProp.description == data["description"]
    del dhdProp


def delete_test():
    """
    Finally, we delete it from the table.
    """
    dhdProp = gateModel(id=data["id"])
    assert dhdProp.delete()
    del dhdProp


def load_delete_test():
    """
    And make sure that if we try to get that object after it's been deleted,
    that we get a new object rather than the existing one we deleted.
    """
    dhdProp = gateModel(id=data["id"])
    assert not hasattr(dhdProp, "what")


"""
------------------------------------------------
Exception raising tests. These should raise an exception of some sort, and if
they don't, then we should fail the test.

Use of @nst.raises() from nose.tools is highly recommended.
"""


@nst.raises(Exception)
def insertBadId_test():
    """
    Here we test to make sure that if we give a primary key of type `None`
    that we are raising an exception, if we don't get an exception then
    something is wrong since the primary key shouldn't be allowed to be `None`
    """
    oldProp = gateModel(id=None, what="Something?")
    assert oldProp.save()
    del oldProp
