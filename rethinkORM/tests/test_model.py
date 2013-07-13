#!/usr/bin/env python
"""
Test suite for the model
"""
import rethinkdb as r
import nose.tools as nst

from rethinkORM import RethinkModel


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
    "description": """Dial Home Device from the planet P3X-439, where an
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

classmethodData = {
    "what": "Stuff",
    "description": "zzzz",
    "id": "fucking-Tests"
    }


class base(object):
    """
    Base test object to help automate some of the repetitive work of reloading
    a document to ensure the model matches the test data. Also takes care of
    deleting the document if `cleanupAfter` is `True`
    """
    cleanupAfter = False
    """Should the document created by this test be deleted when over?"""
    loadCheck = True
    """
    Should the document be reloaded and have all it's data checked against?
    """
    whatToLoad = []
    """
    If loadCheck is true, fill this out with strings of the data keys
    to check the model against.
    """

    model = None
    """The model being used for this test"""
    data = None
    """The data being used for this test. Please at least include an ID"""

    def action_test(self):
        self.action()

    # prefixed with b_ to run this right after action because things run alpha
    # order it seems
    def b_load_test(self):
        if self.loadCheck:
            self.load()

    def cleanup_test(self):
        if self.cleanupAfter:
            self.cleanup()

    def action(self):
        """
        Override this with your own function to do whatever you want for the
        test
        """
        pass

    def load(self):
        """
        Override this to do a custom load check. This should find the key you
        created or modified in `action()` and check it's values to ensure
        everything was set correctly. By default this loads the model with the
        test objects `data["id"]` and uses `whatToLoad` to run checks against
        the data and the model.
        """
        item = self.model(self.data["id"])
        assert item.id == self.data["id"]
        for bit in self.whatToLoad:
            assert getattr(item, bit) == self.data[bit]
        del item

    def cleanup(self):
        """
        Override this to set a custom cleanup process. By default this takes
        the key that was generated in `action()` and calls the models
        `.delete()` function.
        """
        item = self.model(self.data["id"])
        item.delete()
        del item


class insert_test(base):
    """
    Tests the basic ability to make a new model instance, and save it to the
    Database
    """
    whatToLoad = ["what", "description", "planet"]
    data = {"what": "DHD",
            "description": "Dial Home Device",
            "planet": baseData["planet"],
            "id": baseData["id"]}
    model = gateModel

    def action(self):
        """
        Creates a new object, and inserts it, using `.save()`
        """
        dhdProp = gateModel(what=self.data["what"],
                            description=self.data["description"],
                            planet=self.data["planet"])
        dhdProp.id = self.data["id"]
        assert dhdProp.save()
        del dhdProp


class modify_test(base):
    """Tests the ability to load, modify and save a model correctly"""
    whatToLoad = ["what", "description", "planet", "episodes"]
    data = baseData
    model = gateModel

    cleanupAfter = True

    def action(self):
        """
        Next, we get the object again, and this time,
        we modify it, and save it.
        """
        dhdProp = gateModel(what=self.data["what"],
                            description=self.data["description"],
                            planet=self.data["planet"])
        dhdProp.id = self.data["id"]
        assert dhdProp.save()
        del dhdProp

        dhdProp = gateModel(self.data["id"])
        dhdProp.what = self.data["what"]
        dhdProp.description = self.data["description"]
        dhdProp.episodes = self.data["episodes"]
        assert dhdProp.save()
        del dhdProp

        @nst.raises(Exception)
        def d_load_delete_test(self):
            """
            And make sure that if we try to get that object after it's been
            deleted, that we get a new object rather than the existing
            one we deleted.
            """
            dhdProp = self.model(self.data["id"])


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
    """
    Make sure that the model raises an Exception when a key and data are
    provided
    """
    prop = gateModel(id="3", what="duh")


"""
Now onto the classmethods and helper functions to ensure things are good to go
"""


class new_classmethod_test(base):
    """
    Tests the new() classmethod of the model
    """
    model = gateModel
    data = classmethodData
    whatToCheck = ["what", "description"]

    cleanupAfter = True

    def action(self):
        prop = gateModel.new(what=self.data["what"],
                             description=self.data["description"])
        prop.id = self.data["id"]
        assert prop.what == self.data["what"]
        assert prop.description == self.data["description"]
        assert prop.id == self.data["id"]
        assert prop.save()


class create_classmethod_test(base):
    """
    Tests the create() classmethod of the model

    Same as the new() classmethod test however we don't have to explicitly
    tell the model to save
    """
    model = gateModel
    data = classmethodData
    whatToCheck = ["what", "description"]

    def action(self):
        prop = gateModel.create(what=self.data["what"],
                                description=self.data["description"],
                                id=self.data["id"])
        assert prop.what == self.data["what"]
        assert prop.description == self.data["description"]
        assert prop.id == self.data["id"]


class find_classmethod_test(base):
    """
    Tests the find() classmethod of the model
    """
    model = gateModel
    data = classmethodData
    whatToCheck = ["what", "description"]
    loadCheck = False
    cleanupAfter = True

    def action(self):
        oldProp = gateModel(what=self.data["what"],
                            description=self.data["description"])
        oldProp.id = self.data["id"]
        oldProp.save()

        prop = gateModel.find(self.data["id"])
        assert prop.what == self.data["what"]
        assert prop.description == self.data["description"]
        assert prop.id == self.data["id"]
