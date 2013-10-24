#!/usr/bin/env python
"""
This module provides the RethinkModel class which provides a base class that
works as a mapper between a rethink document and a Python object.

First, lets setup the basic rethink connection and get a sample database and
table made.
I choose to go with this option, and providing an option for passing the
connection object into the models because I don't quite like the ORMs which
try to fully replace the underlying driver. This also gives a nice easy way
to use standard ReQL for operations that are beyond the scope of the models.
>>> import rethinkdb as r
>>> import rethinkORM.rethinkModel as rm
>>> import rethinkORM.rethinkCollection as rc
>>> conn = r.connect('localhost', 28015)
>>> a = r.db_create("example").run(conn)
>>> conn.use("example")
>>> conn.repl() #doctest: +ELLIPSIS
<rethinkdb.net.Connection ...>

>>> a = r.table_create("stargates").run()

Now we can create a model that we'll be working with.
>>> class Stargate(rm.RethinkModel):
...   table = "stargates"

And now we can create an actual document using this model.
Create is a classmethod that will return a new Stargate object with the ID
of the newly created document, with the passed data. In this case: location,
and description.
>>> earth_gate = Stargate.create(location="Earth", description="The first of\
 two gates found on earth. Found in Egypt")

If you do not call .repl() on the rethinkdb connection, you can also pass conn
to the model like so:
>>> earth_gate = Stargate.create(location="Earth", description="The first of\
 two gates found on earth. Found in Egypt", connection=conn)

If you did not want to immediately save the document upon creation you can
instead call the .new() classmethod:
>>> atlantis_gate = Stargate.new(location="City of Atlantis", description="The\
 gate in the gate room of the lost city of the ancients, reached from\
 Earth by using a ZPM and dialling an additional 9th symbol.")

You can then make changes to this document, and when you are finished,
call save() which will save the document and set the objects ID to the newly
created documents ID.
>>> atlantis_gate.save()
True

Getting a collection of documents is also easy through the use of
RethinkCollection. Simply give RethinkCollection the classref of your model,
in our case `Stargate` and look at the documents property. This will fetch
all of the documents within the table defined by the Stargate model
(`stargates` in this case). RethinkCollection also provides several helpers
such as accepting a pre built ReQL query, limiting of results, sorting the
documents and filtering them based off of field values.
>>> gates = rc.RethinkCollection(Stargate)
>>> gates.documents #doctest: +ELLIPSIS
[<RethinkModel.Stargate ...>, <RethinkModel.Stargate ...>]

>>> a = r.db_drop("example").run()
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
    _protected_items = []
    _conn = None

    table = ""  #: The table which this document object will be stored in
    primary_key = "id"  #: The current primary key of the table

    durability = "soft"
    """Can either be Hard or Soft, and is passed to RethinkDB"""

    def __init__(self, id=None, **kwargs):
        """
        Initializes the main object, if `id` is the only thing passed then we
        assume this document is already in the database and grab its data,
        otherwise we treat it as a new object.

        (Optional, only if not using .repl()) `conn` or `connection` can also
        be passed, which will be used in all the .run() clauses.
        """

        protected_items = dir(self)
        protected_items.append(self._protected_items)
        self._protected_items = protected_items
        """
        List of strings to not store in the database; automatically set to
        the built in properties of this object to prevent any accidental stuff
        """

        # Is this a new object, or already in the database? (set later)
        self._data = {}  # STORE ALL THE DATA!!

        # If we're given a connection, we'll use it, if not, we'll assume
        # .repl() was called on r.connect()
        if "conn" in kwargs:
            self._conn = kwargs.pop("conn")
        elif "connection" in kwargs:
            self._conn = kwargs.pop("connection")

        key = kwargs[self._primary_key] if self.primary_key in kwargs else id

        if len(kwargs) == 0 and key:
          rawCursor = r.table(self.table).get(key).run(self._conn)
          if rawCursor:
              self._data = dict(rawCursor)

        else:
            for item in kwargs:
                if item not in self._protected_items and item[0] != "_":
                    self._data[item] = kwargs[item]
            self._data[self.primary_key] = key

        # Hook to run any inherited class code, if needed
        self.finish_init()

    def finish_init(self):
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
        if item not in object.__getattribute__(self, "_protected_items") \
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
        if item not in object.__getattribute__(self, "_protected_items") \
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
    def new(cls, id=None, **kwargs):
        """
        Creates a new instance, filling out the models data with the keyword
        arguments passed, so long as those keywords are not in the protected
        items array.
        """
        return cls(id=id, **kwargs)

    @classmethod
    def create(cls, id=None, **kwargs):
        """
        Similar to new() however this calls save() on the object before
        returning it, to ensure that it is already in the database.
        Good for make and forget style calls.
        """
        what = cls(id=id, **kwargs)
        what.save()
        return what

    def save(self):
        """
        Update or insert the document into the database.
        """
        if self.primary_key in self._data and not self._data[self.primary_key]:
            self._data.pop(self.primary_key)

        reply = r.table(self.table) \
            .insert(self._data,
                    upsert=True,
                    durability=self.durability) \
            .run(self._conn)

        if "generated_keys" in reply and reply["generated_keys"]:
            self._data[self.primary_key] = reply["generated_keys"][0]

        if "errors" in reply and reply["errors"] > 0:
            raise Exception("Could not insert entry: %s"
                            % reply["first_error"])

        return True

    def delete(self):
        """
        Deletes the current instance, if its in the database (or try).
        """
        if self.primary_key in self._data:
            r.table(self.table).get(self._data[self.primary_key]) \
                .delete(durability=self.durability).run(self._conn)
            return True
        else:
            raise Exception("Document id not given, cannot delete.")

    def __repr__(self):
        """
        Allows for the representation of the object, for debugging purposes
        """
        return "<RethinkModel.%s at %s with data: %s >" % (self.__class__.__name__,
                                               id(self),
                                               self._data)

    @property
    def protected_items(self):
        """
        Provides a cleaner interface to dynamically add items to the models
        list of protected functions to not store in the database
        """
        return self._protected_items

    @protected_items.setter
    def protected_items(self, value):
        if type(value) is list:
            self._protected_items.extend(value)
        else:
            assert type(value) is str
            self._protected_items.append(value)
        return self._protected_items
