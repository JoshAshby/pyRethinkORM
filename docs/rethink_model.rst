Models
======
The model is the core of everything RethinkORM deals with. All data returned
from RethinkDB is eventually wrapped in the model before being returned to the
end user. It provides an pythonic, object style interface for the data,
exposing methods to save and update documents along with creating new ones.

General Usage
-------------

First we need to make an object which will represent all of our data in
a specific table, along with getting a connection to RethinkDB started.

::

    import rethinkdb as r
    from rethinkORM import RethinkModel

    r.connect(db="props").repl()


    class tvProps(RethinkModel):
        table = "stargate_props"

Inserting/creating an entry
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    dhdProp = tvProps(id="DHD_P3X_439", what="DHD", planet="P3X-439", description="Dial HomeDevice")
    dhdProp.save()

Updating an entry
~~~~~~~~~~~~~~~~~

::

    updatedProp = tvProps("DHD_P3X_439")
    updatedProp.description = """Dial Home Device from the planel P3X-439, where an
        Ancient Repository of Knowledge was found, and interfaced with by Colonel
        Jack."""
    updatedProp.save()

Deleting an entry
~~~~~~~~~~~~~~~~~

::

    oldProp = tvProps("DHD_P3X_439")
    oldProp.delete()

:class:`RethinkORMException`
----------------------------

.. autoclass:: rethinkORM.RethinkORMException

:class:`RethinkModel`
---------------------

.. autoclass:: rethinkORM.RethinkModel
    :members: __init__, finish_init, __delitem__, __contains__, new, create, save, delete, __repr__, protected_items, primary_key, table, durability
    :undoc-members:
    :noindex:
