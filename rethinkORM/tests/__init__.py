import rethinkdb as r


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
