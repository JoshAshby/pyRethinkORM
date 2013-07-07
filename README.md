PyRethinkORM
=============
2013 Joshua Ashby  
joshuaashby (at) joshashby.com  
  
What this is
-------------
  
I recently found RethinkDB and was amazed at how easy everything seemed to be,
however one thing that I've missed is how the data is just a Python `List` or
`Dict` rather than a full wrapper class. So I figured a good way to learn the
general use of the Python RethinkDB driver was to write a general wrapper class
that functioned a bit like an ORM, providing some easier to work with data and
objects.  
  
Warnings
---------
Well, first off: I'm only a second year university student, and software isn't
even my major; I'm working towards an Electrical and Computer Engineering
degree, so not only will I have limited time to keep this maintained, but I
also probably won't write the best code ever. Secondly, this takes some
influence from the [Python Django ORM](https://github.com/dparlevliet/rwrapper)
and other ORM systems, however I haven't really followed a standard pattern for
the interface for this module. If someone wants to make this more standardized
feel free to, and just submit a pull request, I'll look it over and probably
will give it the go ahead.  
  
Docs
----
TODO: Write these. In the mean time, read the source, I've tried to do a
mediocre job of writing some doc strings for everything.  
  
Testing
-------
To get started and make sure this all works, please make sure you have Python
[`nose`](https://github.com/nose-devs/nose) installed.  
  
  cd rethinkORM
  nosetests -s tests/test_model.py -v
  
This will run the tests, not capturing `stdout` and being verbose, in case
anything goes wrong, or if you modify the tests. Please note, tests are subject
to a lot of changes, and this may not always be the same command.  
  
######How the tests work (or should, if more are written):
There is a setup fixture that creates a database called `model` and within that
creates a table `stargate`. Then each test works on entries which get stored
in this database and table. When everything is done, the teardown fixture is
ran to clean up and delete the whole database `model`. Each test should be
broken down into basic actions, for example there are currently tests for:  
 * inserting a new entry
 * modifying that entry
 * deleting that entry
 * inserting an entry where the primary key is `None` or a null value.
  
Contributing
------------
Submit a pull request or open an issue. Most things I probably won't have time
to get around to looking at too deeply, so if you want it fixed, a pull request
is the way to go.  
Besides that, I'm releasing this under the GPLv3 License as found in the
`LICENSE.txt` file. Enjoy!
