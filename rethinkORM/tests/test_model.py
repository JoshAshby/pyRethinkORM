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
    table = "stargate"


# Sample data to use as a comparison as we test the model
baseData = {
    "what": "DHD",
    "description": """Dial Home Device from the planel P3X-439, where an
    Ancient Repository of Knowledge was found, and interfaced with by Colonel
    Jack.""",
    "id": "P3X-439-DHD",
    "planet": "P3X-439",
    "episodes": ["Lost City, Part 1"],
    }


newData = {
    "what": "Star Gate",
    "description": """Device used to form a wormhole to another gate and
    transport matter.""",
    "id": "StarGate-Earth",
    "planet": "Earth",
    "episodes": "All",
    }


class base(object):
    cleanupEntry = False
    model = None
    whatToLoad = []
    data = None
    id = None

    def action_test(self):
        print "action", self
        self.action()

    def b_load_test(self):
        print "load", self
        self.load()

    def cleanup_test(self):
        print "cleanup", self
        if self.cleanupEntry: self.cleanup()

    def action(self):
        pass

    def load(self):
        item = self.model(self.id)
        assert item.id == self.id
        for bit in self.whatToLoad:
              assert getattr(item, bit) == self.data[bit]
        del item

    def cleanup(self):
        item = self.model(self.id)
        item.delete()
        del item


class insert_test(base):
    whatToLoad = ["what", "description", "planet"]
    data = {"what": "DHD",
            "description": "DialHome Device", "planet":
            baseData["planet"]}
    model = gateModel
    id = baseData["id"]

    def action(self):
        """
        Creates a new object, and inserts it, using `.save()`
        """
        dhdProp = gateModel(what="DHD",
                            description="Dial Home Device",
                            planet=self.data["planet"])
        dhdProp.id = self.id
        assert dhdProp.save()
        del dhdProp


class modify_test(base):
    whatToLoad = ["what", "description", "planet", "episodes"]
    data = baseData
    model = gateModel
    id = baseData["id"]

    cleanupEntry = True

    def action(self):
        """
        Next, we get the object again, and this time, we modify it, and save it.
        """
        dhdProp = gateModel(self.id)
        dhdProp.what = self.data["what"]
        dhdProp.description = self.data["description"]
        dhdProp.episodes = self.data["episodes"]
        assert dhdProp.save()
        del dhdProp


"""
------------------------------------------------
Exception raising tests. These should raise an exception of some sort, and if
they don't, then we should fail the test.

Use of @nst.raises() from nose.tools is highly recommended.
"""


@nst.raises(Exception)
def load_delete_test():
    """
    And make sure that if we try to get that object after it's been deleted,
    that we get a new object rather than the existing one we deleted.
    """
    dhdProp = gateModel(data["id"])


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


@nst.raises(Exception)
def insertIdAndData_test():
    prop = gateModel(id="3", what="duh")


"""
Now onto the classmethods and helper functions to ensure things are good to go
"""


def new_classmethod_test():
    prop = gateModel.new(what=newData["what"],
                        description=newData["description"])
    prop.id = newData["id"]
    assert prop.what == newData["what"]
    assert prop.description == newData["description"]
    assert prop.id == newData["id"]
    assert prop.save()


def load_new_classmethod_test():
    prop = gateModel(newData["id"])
    assert prop.what == newData["what"]
    assert prop.description == newData["description"]
    assert prop.id == newData["id"]
