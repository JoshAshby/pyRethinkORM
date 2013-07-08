#!/usr/bin/env python
"""
ALL THE TESTS!!!

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import rethinkdb as r
import rethinkdb.errors as rerr
import nose.tools as nst
import rethinkModel as rdbm


"""
################################################
Test Fixtures, setup and teardown run before the first test, and after the last
test, respectfully. These are responsable for initializing the RethinkDB
connection, making a test database, and later destroying that test database.

gateModel is the test object that we'll be working with
"""
def setup():
    conn = r.connect('localhost', 28015)
    r.db_create("model").run(conn)
    conn.use("model")
    conn.repl()
    r.table_create("stargate").run()

def teardown():
    #r.db_drop("model").run()
    pass


class gateModel(rdbm.RethinkModel):
    _table = "stargate"


"""
################################################
Start Unittests
"""
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
    dhdProp = gateModel(what="DHD", description="Dial Home Device",
        planet=data["planet"], id=data["id"])
    assert dhdProp.save()
    del dhdProp

def load_insert_test():
    dhdProp = gateModel.load(data["id"])
    print dhdProp
    assert dhdProp.id == data["id"]
    assert dhdProp.what == "DHD"
    assert dhdProp.planet == data["planet"]
    del dhdProp

def modify_test():
    dhdProp = gateModel(id=data["id"])
    dhdProp.what = data["what"]
    dhdProp.description = data["description"]
    dhdProp.episodes = data["episodes"]
    assert dhdProp.save()
    del dhdProp

def load_modify_test():
    dhdProp = gateModel.load(data["id"])
    assert dhdProp.id == data["id"]
    assert dhdProp.what == data["what"]
    assert dhdProp.planet == data["planet"]
    assert dhdProp.episodes == data["episodes"]
    assert dhdProp.description == data["description"]
    del dhdProp

def delete_test():
    dhdProp = gateModel(id=data["id"])
    assert dhdProp.delete()
    del dhdProp

#@nst.raises()
def load_delete_test():
    dhdProp = gateModel(id=data["id"])

"""
------------------------------------------------
Exception raising tests. These should raise an exception of some sort, and if
they don't, then we should fail the test.

Use of @nst.raises() from nose.tools is highly recommended.
"""
@nst.raises(Exception)
def insertBadId_test():
    oldProp = gateModel(id=None, what="Something?")
    assert oldProp.save()
    del oldProp
