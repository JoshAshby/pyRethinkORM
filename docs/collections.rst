..  _collections:

RethinkCollection
=================

Collections provide a quick and easy way to interact with many documents of the
same type all at once. They also provide a mechanism for basic joins across one
addition table (due to current limitations of RethinkDB and how it handles
joins). Collections act like Lists of RethinkModel objects, but provide an
interface to order the results, and optionally, eqJoin across one other table,
along with filtering of results.

Initialize a new Collection
----------------------------
Optionally you can also pass a dictionary which will be used as a filter. For
more information on how filters work, please see the `RethinkDB docs <http://www.rethinkdb.com/api/#py:selecting_data-filter>`__

::

    collection = RethinkCollection(gateModel)


Join on a table
---------------

::

    collection.joinOn(episodeModel, "episodes")


Order the Results
-----------------

::

    collection.orderBy("episodes", "ASC")


Finally, Fetch the Results
--------------------------

::

    result = collection.fetch()

Result acts like a List, containing all of the Documents which are part of the
collection, all pre wrapped in a RethinkModel object.


:mod:`rethinkCollection` Module
-------------------------------

.. autoclass:: rethinkORM.rethinkCollection.RethinkCollection
    :members: __init__, joinOn, joinOnAs, orderBy, fetch
    :undoc-members:
    :noindex:

Subpackages
-----------

.. toctree::

    rethinkORM.tests
