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
