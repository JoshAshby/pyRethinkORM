RethinkORM: Introduction
========================

Build status - Master:


.. image:: https://secure.travis-ci.org/JoshAshby/pyRethinkORM.png?branch=master
        :target: http://travis-ci.org/JoshAshby/pyRethinkORM

.. image:: https://pypip.in/v/RethinkORM/badge.png
    :target: https://crate.io/packages/RethinkORM/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/RethinkORM/badge.png
    :target: https://crate.io/packages/RethinkORM/
    :alt: Number of PyPI downloads


Build status - Dev:


.. image:: https://secure.travis-ci.org/JoshAshby/pyRethinkORM.png?branch=dev
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


Installation:
-------------
This package is kindly hosted on the Python Package Index making it as easy as
a simple ``pip`` command to install.

::

    pip install RethinkORM


Quick Start
-----------
There are currently two main modules to this package, Models and Collections.

`Models <models.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~
The core of RethinkORM, models are the main unit of code you'll probably be use
from this package.

`Collections <collections.html>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
New in v0.2.0 are collections. These are containers for interacting with sets
of documents. Collections provide an easy way to gather up just the documents
you need, and have them automatically wrapped with the ORM RethinkModel object.

You can read more about `collections here <collections.html>`__.

Versioning
~~~~~~~~~~
This project will try to follow the semantic versioning guide lines, as laid
out here: `SemVer <http://semver.org/>`__, as best as possible.

Contributing
------------

All code for this can be found online at
`github <https://github.com/JoshAshby/pyRethinkORM>`__.
If something is broken, or a feature is missing, please submit a pull request
or open an issue. Most things I probably won't have time to get around to
looking at too deeply, so if you want it fixed, a pull request is the way
to go. Besides that, I'm releasing this under the GPLv3 License as found in the
``LICENSE.txt`` file. Enjoy!


Doc Contents
------------

.. toctree::
   :maxdepth: 4

   model
   collections
   rethinkORM.tests
   rethinkORM


Indices and tables
~~~~~~~~~~~~~~~~~~

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
