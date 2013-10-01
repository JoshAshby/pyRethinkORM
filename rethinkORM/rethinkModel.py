#!/usr/bin/env python
"""
ORM style interface for working with RethinkDB and having a native wrapper and
some helper functions for working with the wrapper. This module contains
the base model which should be inherited.
"""
import rethinkdb as r


class RethinkModel(object):
    """
    Emulates a python object for the  data which is returned from rethinkdb and
    the official Python client driver. Raw data from the database is stored in
    _data to keep the objects namespace clean. For more information look at how
    _get() and _set() function in order to keep the namespace cleaner but still
    provide easy access to data.

    This object has a __repr__ method which can be used with print or logging
    statements. It will give the id and a representation of the internal _data
    dict for debugging purposes.
    """
    _protectedItems = []
    _conn = None
    _join = None
    _joinedField = ""

    table = ""  #: The table which this document object will be stored in
    primaryKey = "id"  #: The current primary key of the table

    durability = "soft"
    """Can either be Hard or Soft, and is passed to RethinkDB"""

    non_atomic = False
    """Determins if the transaction can be non atomic or not"""

    upsert = True
    """Will either update, or create a new object if true and a primary key is
    given."""

    def __init__(self, id=False, **kwargs):
        """
        Initializes the main object, if `id` is in kwargs, then we assume
        this is already in the database, and will try to pull its data, if not,
        then we assume this is a new entry that will be inserted.

        (Optional, only if not using .repl()) `conn` or `connection` can also
        be passed, which will be used in all the .run() clauses.
        """

        protectedItems = dir(self)
        protectedItems.append(self._protectedItems)
        self._protectedItems = protectedItems
        """
        List of strings to not store in the database; automatically set to
        the built in properties of this object to prevent any accidental stuff
        """

        # Is this a new object, or already in the database? (set later)
        self._new = True
        self._data = {}  # STORE ALL THE DATA!!

        # If we're given a connection, we'll use it, if not, we'll assume
        # .repl() was called on r.connect()
        self._conn = kwargs.pop("conn", kwargs.pop("connection", None))

        key = kwargs.get(self.primaryKey, id)

        if key is None or key == "" and len(kwargs) == 0:
            raise Exception("""Cannot have an empty or type None key""")

        elif key and len(kwargs) > 0:
            # Assume we have data from a collection, just go with it and set
            # our data.
            #self._makeNew(kwargs)
            raise Exception("""Cannot supply primary key and additional \
arguments while searching for Documents.""")

        if key and not self._grabData(key):
            raise Exception("""Could not find key in database""")

        self._makeNew(kwargs)
        if key:
            self._data[self.primaryKey] = key

        # Hook to run any inherited class code, if needed
        self.finishInit()

    def _makeNew(self, kwargs):
        # We assume this is a new object, and that we'll insert it
        for key in kwargs:
            if key not in object.__getattribute__(self, "_protectedItems") \
                   or key[0] != "_":
                self._data[key] = kwargs[key]

    def _grabData(self, key):
        """
        Tries to find the existing document in the database, if it is found,
        then the objects _data is set to that document, and this returns
        `True`, otherwise this will return `False`

        :param key: The primary key of the object we're looking for
        :type key: Str

        :return: True if a document was found, otherwise False
        :rtype: Boolean
        """
        rawCursor = r.table(self.table).get(key).run(self._conn)
        if rawCursor:
            self._data = rawCursor
            self._new = False
            return True
        else:
            return False

    def finishInit(self):
        """
        A hook called at the end of the main `__init__` to allow for
        custom inherited classes to customize their init process without having
        to redo all of the existing int.
        This should accept nothing besides `self` and nothing should be
        returned.
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

        Will only set the objects _data if the given items name is not prefixed
        with _ or if the item exists in the protected items List.
        """
        if item not in object.__getattribute__(self, "_protectedItems") \
                and item[0] != "_":
            keys = object.__getattribute__(self, "_data")
            if not hasattr(value, '__call__'):
                keys[item] = value
                return value
            if hasattr(value, '__call__') and item in keys:
                raise Exception("""Cannot set model data to a function, same \
name exists in data""")
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
        """
        Deletes the given item from the objects _data dict, or if from the
        objects namespace, if it does not exist in _data.
        """
        keys = object.__getattribute__(self, "_data")
        if item in keys:
            del(keys[item])
        else:
            object.__delitem__(self, item)

    def __contains__(self, item):
        """
        Allows for the use of syntax similar to::

            if "blah" in model:

        This only works with the internal _data, and does not include other
        properties in the objects namepsace.
        """
        keys = object.__getattribute__(self, "_data")
        if item in keys:
            return True
        return False

    @classmethod
    def fromRawEntry(cls, **kwargs):
        """
        Helper function to allow wrapping existing data/entries, such as
        those returned by collections.
        """
        id = kwargs["id"]

        kwargs.pop("id")

        what = cls(**kwargs)
        what._new = False
        what.id = id

        return what

    @classmethod
    def new(cls, **kwargs):
        """
        Creates a new instance, filling out the models data with the keyword
        arguments passed, so long as those keywords are not in the protected
        items array.
        """
        return cls(**kwargs)

    @classmethod
    def create(cls, id=None, **kwargs):
        """
        Similar to new() however this calls save() on the object before
        returning it.
        """
        what = cls(**kwargs)
        if id:
            setattr(what, cls.primaryKey, id)
        what.save()
        return what

    @classmethod
    def find(cls, id):
        """
        Loads an existing entry if one can be found, otherwise an exception is
        raised.

        :param id: The id of the given entry
        :type id: Str

        :return: `cls` instance of the given `id` entry
        """
        return cls(id)

    def save(self):
        """
        If an id exists in the database, we assume we'll update it, and if not
        then we'll insert it. This could be a problem with creating your own
        id's on new objects, however luckily, we keep track of if this is a new
        object through a private _new variable, and use that to determine if we
        insert or update.
        """
        if not self._new:
            data = self._data.copy()
            ID = data.pop(self.primaryKey)
            reply = r.table(self.table).get(ID) \
                .update(data,
                        durability=self.durability,
                        non_atomic=self.non_atomic) \
                .run(self._conn)

        else:
            reply = r.table(self.table) \
                .insert(self._data,
                        durability=self.durability,
                        upsert=self.upsert) \
                .run(self._conn)
            self._new = False

        if "generated_keys" in reply and reply["generated_keys"]:
            self._data[self.primaryKey] = reply["generated_keys"][0]

        if "errors" in reply and reply["errors"] > 0:
            raise Exception("Could not insert entry: %s"
                            % reply["first_error"])

        return True

    def delete(self):
        """
        Deletes the current instance. This assumes that we know what we're
        doing, and have a primary key in our data already. If this is a new
        instance, then we'll let the user know with an Exception
        """
        if self._new:
            raise Exception("This is a new object, %s not in data, \
indicating this entry isn't stored." % self.primaryKey)

        r.table(self.table).get(self._data[self.primaryKey]) \
            .delete(durability=self.durability).run(self._conn)
        return True

    def __repr__(self):
        """
        Allows for the representation of the object, for debugging purposes
        """
        return "< %s at %s with data: %s >" % (self.__class__.__name__,
                                               id(self),
                                               self._data)

    @property
    def protectedItems(self):
        """
        Provides a cleaner interface to dynamically add items to the models
        list of protected functions to not store in the database
        """
        return self._protectedItems

    @protectedItems.setter
    def protectedItems(self, value):
        if type(value) is list:
            self._protectedItems.extend(value)
        else:
            assert type(value) is str
            self._protectedItems.append(value)
        return self._protectedItems
