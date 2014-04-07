Collections
===========
Collections provide a quick and easy way to interact with many documents of the
same type all at once. They also provide a mechanism for basic joins across one
addition table (due to current limitations of RethinkDB and how it handles
joins). Collections act like python `lists` of :py:class:`.RethinkModel`
objects, but provide an easy interface to order, filter, and limit the results.

General Usage
-------------
Collections are pretty simplistic objects. Just instantiate a new object with
the model which you are constructing the collection from.

::

    collection = RethinkCollection(gateModel)


.. note::
    Optionally you can also pass a dictionary which will be used as a filter. For
    more information on how filters work, please see the `RethinkDB docs <http://www.rethinkdb.com/api/#py:selecting_data-filter>`__

Order the Results
~~~~~~~~~~~~~~~~~

::

    collection.orderBy("episodes", "ASC")

Limit the Results
~~~~~~~~~~~~~~~~~

::

    collection.limit(10, 5) # Limit to 10 results, starting after the 5th one.

Fetch the Results
~~~~~~~~~~~~~~~~~

::

    result = collection.fetch()

`result` acts like a bit like a normal python `list`, containing all of the
documents which are part of the collection, all pre-wrapped in a
:py:class:`.RethinkModel` object.

:class:`RethinkCollection`
--------------------------

.. autoclass:: rethinkORM.RethinkCollection
    :members: __init__, order_by, limit, fetch
    :undoc-members:
    :noindex:
