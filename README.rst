PyRethinkORM
============

| 2013 Joshua Ashby
| joshuaashby (at) joshashby.com

What this is
------------

I recently found RethinkDB and was amazed at how easy everything seemed
to be, however one thing that I've missed is how the data is just a
Python ``List`` or ``Dict`` rather than a full wrapper class. So I
figured a good way to learn the general use of the Python RethinkDB
driver was to write a general wrapper class that functioned a bit like
an ORM, providing some easier to work with data and objects.

Warnings
--------

Well, first off: I'm only a second year university student, and software
isn't even my major; I'm working towards an Electrical and Computer
Engineering degree, so not only will I have limited time to keep this
maintained, but I also probably won't write the best code ever.
Secondly, this takes some influence from the `Python Django RethinkDB
ORM <https://github.com/dparlevliet/rwrapper>`__ and other ORM systems,
however I haven't really followed a standard pattern for the interface
for this module. If someone wants to make this more standardized feel
free to, and just submit a pull request, I'll look it over and probably
will give it the go ahead.

Docs
----

First we need to make an object which will represent all of our data in
a specific table:

::

    class tvProps(rdbm.RethinkModel):
        _table = "stargate_props"

Object properties such as ``_primaryKey`` ``_protectedItems``
``_dirability`` and ``_non_atomic`` can also be set here, or per object
once initialized.

Any property or function which is added to the model, can be prefixed
with a ``_`` to avoid having it inserted into the database, or it can be
added to the ``list`` ``_protectedItems``.

When initializing a new object, keyword arguments are assumed to be data
for the model, unless they fit the above "protected items" pattern. If
the ``_primaryKey`` is passed in while initializing, then the model will
assume we're grabbing an existing entry and try to get that entry from
the database, if none is found then it will act like a new entry.

By default ``_primaryKey`` is set to ``id`` however if you changed what
the primary index of your table is, this property should match that
index's name.

Getting ready
~~~~~~~~~~~~~

::

    r.connect(db="props").repl()

Inserting/creating an entry
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    dhdProp = tvProps(what="DHD", planet="P3X-439", description="Dial HomeDevice",
        id="DHD_P3X_439")
    dhdProp.save()

Updating an entry
~~~~~~~~~~~~~~~~~

::

    updatedProp = tvProps(id="DHD_P3X_439")
    updatedProp.description="""Dial Home Device from the planel P3X-439, where an
        Ancient Repository of Knowledge was found, and interfaced with by Colonel
        Jack."""
    updatedProp.save()

Deleting an entry
~~~~~~~~~~~~~~~~~

::

    oldProp = tvProps(id="DHD_P3X_439")
    oldProp.delete()

Testing
-------

To get started and make sure this all works, please make sure you have
Python `nose <https://github.com/nose-devs/nose>`__ installed.

::

    cd rethinkORM  
    nosetests -s tests/test_model.py -v

This will run the tests, not capturing ``stdout`` and being verbose, in
case anything goes wrong, or if you modify the tests. Please note, tests
are subject to a lot of changes, and this may not always be the same
command.

How the tests work (or should, if more are written):
                                                    

| There is a setup fixture that creates a database called ``model`` and
within that creates a table ``stargate``. Then each test works on
entries which get stored in this database and table. When everything is
done, the teardown fixture is ran to clean up and delete the whole
database ``model``. Each test should be broken down into basic actions,
for example there are currently tests for:
|  \* inserting a new entry \* modifying that entry \* deleting that
entry \* inserting an entry where the primary key is ``None`` or a null
value.

Contributing
------------

| Submit a pull request or open an issue. Most things I probably won't
have time to get around to looking at too deeply, so if you want it
fixed, a pull request is the way to go.
| Besides that, I'm releasing this under the GPLv3 License as found in
the ``LICENSE.txt`` file. Enjoy!
