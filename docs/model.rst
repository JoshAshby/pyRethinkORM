..  _model:

RethinkModel
============

The model is the core of everything RethinkORM deals with. All data returned
from RethinkDB is eventually wrapped in the model before being returned to the
end user. It provides an pythonic, object style interface for the data,
exposing methods to save and update documents along with creating new ones.

Quick Start:
------------

::

    pip install RethinkORM

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


:mod:`rethinkModel` Module
--------------------------

.. autoclass:: rethinkORM.rethinkModel.RethinkModel
    :members: __init__, finishInit, __delitem__, __contains__, new, find, save, delete, __repr__, protectedItems, primaryKey, table, durability, non_atomic, upsert, create
    :undoc-members:
    :noindex:
