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


Documentation
=============

For more information, a short quick start, and information about running the
test suit, please `read the documentation
<https://rethinkorm.readthedocs.org/en/latest/>`__ kindly hosted
on `readthedocs.org <http://readthedocs.org>`__

Contributing
------------

Submit a pull request or open an issue. Most things I probably won't have
time to get around to looking at too deeply, so if you want it fixed, a pull
request is the way to go.
Besides that, I'm releasing this under the GPLv3 License as found in the
``LICENSE.txt`` file. Enjoy!
