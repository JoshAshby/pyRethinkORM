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


dhdProp = None
def insert_test():
    dhdProp = gateModel(what="DHD", description="Dial Home Device",
        planet="P3X-439", id="P3X-439-DHD")
    assert dhdProp.save()

def delete_test():
    newDhdProp = gateModel(id="P3X-439-DHD")
    newDhdProp.delete()

@nst.raises(Exception)
def insertBadId_test():
    oldProp = gateModel(id=None, what="Something?")
    assert oldProp.save()
