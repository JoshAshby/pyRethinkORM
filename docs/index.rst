.. RethinkORM documentation master file, created by
   sphinx-quickstart on Mon Jul  8 22:56:50 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

RethinkORM
==========

.. image:: https://secure.travis-ci.org/JoshAshby/pyRethinkORM.png?branch=master
        :target: http://travis-ci.org/JoshAshby/pyRethinkORM

RethinkORM is a small wrapper class to help make working with documents in
`RethinkDB <http://www.rethinkdb.com/>`__ easier, and in a more Pythonic way.

I recently found RethinkDB and was amazed at how easy everything seemed
to be, however one thing that I've missed is how the data is just a
Python ``List`` or ``Dict`` rather than a full wrapper class. So I
figured a good way to learn the general use of the Python RethinkDB
driver was to write a general wrapper class that functioned a bit like
an ORM, providing some easier to work with data and objects.

A Few Minor Warnings
--------------------

#. I'm only a second year university student, and software
   isn't even my major; I'm working towards an Electrical and Computer
   Engineering degree, so not only do I have limited time to keep this
   maintained, but I also probably won't write the best code ever.
#. This takes some influence from the `Python Django RethinkDB 
   ORM <https://github.com/dparlevliet/rwrapper>`__ and other ORM systems,
   however I haven't really followed a standard pattern for the interface
   for this module. If someone wants to make this more standardized feel
   free to, and just submit a pull request, I'll look it over and probably
   will give it the go ahead. For more information see below.
#. This is a very early release, things might break, and the code is honestly a
   little childish at best. In other words: It'll hopefully get better, but it
   might be a little limited right now.

Quick Start:
------------

First we need to make an object which will represent all of our data in
a specific table, along with getting a connection to RethinkDB started.

::

    import rethinkdb as r
    from rethinkORM import RethinkModel

    r.connect(db="props").repl()


    class tvProps(RethinkModel):
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


Contributing
------------

Submit a pull request or open an issue. Most things I probably won't have
time to get around to looking at too deeply, so if you want it fixed, a pull
request is the way to go.
Besides that, I'm releasing this under the GPLv3 License as found in the
``LICENSE.txt`` file. Enjoy!


Doc Contents
------------

.. toctree::
   :maxdepth: 4

   rethinkORM


Indices and tables
~~~~~~~~~~~~~~~~~~

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

