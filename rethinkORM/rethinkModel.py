#!/usr/bin/env python
"""
ORM style interface for working with RethinkDB and having a native wrapper and
    some helper functions

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import rethinkdb as r


class RethinkModel(object):
    """
    Emulates a python object for the  data which is returned from rethinkdb and
    the official Python client driver.
    """
    _protectedItems = []
    _table = ""
    _primaryKey = "id"
    _conn = None

    _durability = "soft"
    _non_atomic = False

    def __init__(self, **kwargs):
        """
        Initializes the main object, if `id` is in kwargs, then we assume
        this is already in the database, and will try to pull its data, if not,
        then we assume this is a new entry that will be inserted.

        (Optional, only if not using .repl()) `conn` or `connection` can also
        be passed, which will be used in all the .run() clauses.
        """
        self._data = {}

        # If we're given a connection, we'll use it, if not, we'll assume
        # .repl() was called on r.connect()
        if hasattr(kwargs, "conn") or hasattr(kwargs, "connection"):
            self._conn = kwargs["conn"]

        whatToDo = False

        if self._primaryKey in kwargs and kwargs[self._primaryKey] != None:
            key = kwargs[self._primaryKey]
            whatToDo = self._grabData(key)

        # This is a no-no
        elif self._primaryKey in kwargs and kwargs[self._primaryKey] == None:
            raise Exception("%s supplied but with type `None`" % self._primaryKey)

        if not whatToDo:
            # We assume this is a new object, and that we'll insert it
            for key in kwargs:
                if key not in ["conn", "connection"] or key[0] != "_":
                    self._data[key] = kwargs[key]

        # Hook to run any inherited class code, if needed
        self._finishInit()

    def _grabData(self, key):
        rawCursor = r.table(self._table).get(key).run(self._conn)
        if rawCursor:
            self._data = [ item for item in rawCursor ][0]
            return True
        else:
            return False

    def _finishInit(self):
        """
        A hook called at the end of the main ``__init__` to allow for
        custom inherited classes to customize their init.
        """
        pass

    def _get(self, item):
        """
        Helper function to keep the __getattr__ and __getitem__ calls
        KISSish
        """
        if item not in object.__getattribute__(self, "_protectedItems") \
                and item[0] != "_":
            data = object.__getattribute__(self, "_data")
            if item in data:
                return data[item]
        return object.__getattribute__(self, item)

    def _set(self, item, value):
        """
        Helper function to keep the __setattr__ and __setitem__ calls
        KISSish

        Will only set the objects data if the given items name is not prefixed
        with _ or if the item exists in the protected items List.
        """
        if item not in object.__getattribute__(self, "_protectedItems") \
                and item[0] != "_":
            keys = object.__getattribute__(self, "_data")
            if not hasattr(value, '__call__'):
                keys[item] = value
                return value
            if hasattr(value, '__call__') and item in keys:
                raise Exception("Function exists in object with same name,\
                    skipping setting property.")
        return object.__setattr__(self, item, value)

    def __getattr__(self, item):
        return self._get(item)

    def __getitem__(self, item):
        return self._get(item)

    def __setattr__(self, item, value):
        return self._set(item, value)

    def __setitem__(self, item, value):
        return self._set(item, value)

    def __delitem__(self, item):
        keys = object.__getattribute__(self, "_data")
        if item in keys:
            del(keys[item])
        else:
            object.__delitem__(self, item)

    def __contains__(self, item):
        keys = object.__getattribute__(self, "_data")
        if item in keys:
            return True
        return False

    @classmethod
    def new(cls, **kwargs):
        """
        Gathers, or creates a new record with the given kwargs. If `id`
        exists in `kwargs` then this will assume that your pulling an existing
        entry from the database
        """
        return cls(**kwargs)

    def load(cls, id):
        """
        Loads an existing entry.

        :param id: The id of the given entry
        :type id: Str

        :return: `cls` instance of the given `id` entry
        """
        key = cls._primaryKey
        data = {key: id}
        return cls(**data)

    def save(self):
        """
        If an id exists in the database, we assume we'll update it, and if not
        then we'll insert it. This could be a problem with creating your own
        id's on new objects, but that could be solved by setting a `_new`
        property or something.
        """
        if self._primaryKey in self._data:
            reply = r.table(self._table).update(self._data,
                durability=self._durability,
                non_atomic=self._non_atomic).run(self._conn)
        else:
            reply = r.table(self._table).insert(self._data,
                durability=self._durability).run(self._conn)

        if "errors" in reply and reply["errors"] > 0:
            raise Exception("Could not insert entry: %s" % reply["first_error"])

        return True

    def delete(self):
        """
        Deletes the current instance. This assumes that we know what we're
        doing, and have a primary key in our data already. If this is a new
        instance, then we'll let the user know with an Exception
        """
        if self._primaryKey not in self._data:
            raise Exception("%s not in data, indicating this entry isn't \
                stored." % self._primaryKey)

        r.table(self._table).get(self._data[self._primaryKey]).delete(durability=self._durability).run(self._conn)
