tests Package
=============

To get started and make sure this all works, please make sure you have
Python `nose <https://github.com/nose-devs/nose>`__ installed.

::

    nosetests -s rethinkORM/tests -v

This will run the all the tests, not capturing ``stdout`` and being verbose, in
case anything goes wrong, or if you modify the tests. Please note, tests
are subject to a lot of changes, and this may not always be the same
command.

How the tests work (or should, if more are written):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| There is a setup fixture that creates a database called ``model`` and
within that creates a table ``stargate``. Then each test works on
entries which get stored in this database and table. When everything is
done, the teardown fixture is ran to clean up and delete the whole
database ``model``. Each test should be broken down into basic actions,
for example there are currently tests for:
* inserting a new entry 
* modifying that entry 
* deleting that entry 
* inserting an entry where the primary key is ``None`` or a null value. 

:mod:`test_model` Module
------------------------

.. automodule:: rethinkORM.tests.test_model
    :members:
    :undoc-members:
    :show-inheritance:

