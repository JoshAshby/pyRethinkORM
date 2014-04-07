RethinkORM v1.0.0 - DEV
=======================

Master:

.. image:: http://img.shields.io/travis/JoshAshby/pyRethinkORM/master.svg
    :target: http://travis-ci.org/JoshAshby/pyRethinkORM
    :alt: Travis-Ci build status

.. image:: http://img.shields.io/coveralls/JoshAshby/pyRethinkORM/master.svg
    :target: https://coveralls.io/r/JoshAshby/pyRethinkORM
    :alt: Coveralls test coverage

.. image:: https://img.shields.io/pypi/v/RethinkORM.svg
    :target: https://pypi.python.org/pypi/RethinkORM/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/d/RethinkORM.svg
    :target: https://pypi.python.org/pypi/RethinkORM/
    :alt: Number of PyPI downloads

.. image:: http://img.shields.io/gittip/JoshAshby.svg
    :target: https://www.gittip.com/JoshAshby
    :alt: JoshAshby's Gittip donations

Dev:

.. image:: http://img.shields.io/travis/JoshAshby/pyRethinkORM/dev.svg
    :target: http://travis-ci.org/JoshAshby/pyRethinkORM
    :alt: Travis-ci dev branch build status

RethinkORM is a small wrapper class to help make working with documents in
`RethinkDB <http://www.rethinkdb.com/>`__ easier, and in a more Pythonic way.

When I found RethinkDB, I was amazed at how easy everything seemed
to be, however one thing that I missed was how the data was just a
Python `list` or `dict` rather than a full wrapper class. So I
figured a good way to learn the general use of the Python RethinkDB
driver was to write a general wrapper class that functioned a bit like
an ORM, providing some easier to work with data and objects.

Changes from Version 0.2.0
--------------------------

#. Relicensed from GPL v3 to MIT.
#. Several names have changed, primarially: `protectedItems` is now
   `protected_items`, `primaryKey` is now `primary_key`, `orderBy` in collections is now `order_by`. There are probably others that I'm missing however.
#. The ability to join tables or models within a collection have been removed
   for now (it was mostly broken anyways).
#. The find classmethod on models has been removed (For now, until I come up
   with a better way of doing this).
#. `fromRawEntry` is not outdated, and can be replaced by just instantiating a
   new model with the data.
#. The models no longer keep track of if a document is new and just use the
   RethinkDB drivers `upsert` ability to insert or update a document.
#. Passing a key and data will now no longer raise an exception, but instead
   return a new model.
#. Providing only `id` as a keyword argument to the model will cause it to
   assume the document is in the database, and it will attempt to get that
   document.

A Few Minor Warnings
--------------------

#. I am a second year university student working towards a Computer
   Engineering degree, so not only do I have limited time to keep this
   maintained, but I also probably won't write the best code ever.
#. This takes some influence from the `Python Django RethinkDB 
   ORM <https://github.com/dparlevliet/rwrapper>`__ and other ORM systems,
   however I haven't really followed a standard pattern for the interface
   for this module. If someone wants to make this more standardized feel
   free to, and just submit a pull request, I'll look it over and probably
   will give it the go ahead. For more information see below.
#. While this is now on its second major version, the code is still maturing a
   bit so chances are stuff will still break. Again, see below for information
   about contributing patches or features.

Installation:
-------------

::

    pip install RethinkORM

For more information, a short quick start, and information about running the
test suit, please `read the documentation
<https://rethinkorm.readthedocs.org/en/latest/>`__ kindly hosted
on `readthedocs.org <http://readthedocs.org>`__

Contributing
------------

All code for this can be found online at
`github <https://github.com/JoshAshby/pyRethinkORM>`__.
If something is broken, or a feature is missing, please submit a pull request
or open an issue. Most things I probably won't have time to get around to
looking at too deeply, so if you want it fixed, a pull request is the way
to go. In your pull request please provide an explaniation as to what your
request is for, and what benefit it provides. Also please try to follow `PEP8 
<http://www.python.org/dev/peps/pep-0008/>`__ as best a possible.

Unittests are included in the `tests/` directory and are ran every commit
thanks to `travis-ci.org <http://travis-ci.org>`__ and this documentation
is kindly hosted and automatically rebuilt by `readthedocs.org
<http://readthedocs.org>`__. Test coverage is also provided by `coveralls.io
<https://coveralls.io/>`__.

If you would like to run the tests on your own all you have to do is::

    nosetests

.. note::
    Tests require nose and coverage to be installed.

License
-------
This is released this under the MIT License as found in the
``LICENSE.txt`` file. Enjoy!

.. warning::
    Heads up, version 1.0.0 has a different license than previous releases: The
    pre v1.0.0 releases were licensed under the GPL v3 License.

Versioning
~~~~~~~~~~
This project will try to follow the semantic versioning guide lines, as laid
out here: `SemVer <http://semver.org/>`__, as best as possible.

Thanks
~~~~~~
Shout outs to these people for contributing to the project:

#. `scragg0x <https://github.com/scragg0x>`__
#. `grieve <https://github.com/grieve>`__


