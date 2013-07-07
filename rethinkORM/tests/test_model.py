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


class gateModel(rdbm.RethinkModel):
    _table = "stargate"


def setup():
    conn = r.connect('localhost', 28015)
    r.db_create("model").run(conn)
    conn.use("model")
    conn.repl()
    r.table_create("stargate").run()

def teardown():
    r.db_drop("model").run()


def insert_test():
    dhdProp = gateModel(what="DHD", description="Dial Home Device",
        planet="P3X-439", id="P3X-439-DHD")
    assert dhdProp.save()

def modify_test():
    dhdProp = gateModel(id="P3X-439-DHD")
    dhdProp.what = "DHD P3X-439"
    dhdProp.description = """Dial Home Device from the planel P3X-439, where an
    Ancient Repository of Knowledge was found, and interfaced with by Colonel
    Jack."""
    dhdProp.episode = ["Lost City, Part 1"]
    assert dhdProp.save()

def delete_test():
    dhdProp = gateModel(id="P3X-439-DHD")
    assert dhdProp.delete()

@nst.raises(Exception)
def insertBadId_test():
    oldProp = gateModel(id=None, what="Something?")
    assert oldProp.save()
