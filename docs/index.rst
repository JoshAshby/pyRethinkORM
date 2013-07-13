RethinkORM: Introduction
========================

Build status:

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

Unittests are included, and the code should be `PEP8 
<http://www.python.org/dev/peps/pep-0008/>`__ compliant. The tests are
automatically ran each commit, thanks to `travis-ci.org
<http://travis-ci.org>`__ and this documentation is kindly hosted and
automatically rebuilt by `readthedocs.org <http://readthedocs.org>`__.

Gittip if you like the work I do and would consider a small donation to help
fund me and this project:

.. raw:: html

    <iframe style="border: 0; margin: 0; padding: 0;"
        src="https://www.gittip.com/JoshAshby/widget.html"
        width="48pt" height="22pt"></iframe>

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
        table = "stargate_props"


For more information on what class properties are available to change, see
:ref:`rethinkORM`

Inserting/creating an entry
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    dhdProp = tvProps(what="DHD", planet="P3X-439", description="Dial HomeDevice")
    dhdProp.id="DHD_P3X_439"
    dhdProp.save()

Updating an entry
~~~~~~~~~~~~~~~~~

::

    updatedProp = tvProps("DHD_P3X_439")
    updatedProp.description="""Dial Home Device from the planel P3X-439, where an
        Ancient Repository of Knowledge was found, and interfaced with by Colonel
        Jack."""
    updatedProp.save()

Deleting an entry
~~~~~~~~~~~~~~~~~

::

    oldProp = tvProps("DHD_P3X_439")
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
