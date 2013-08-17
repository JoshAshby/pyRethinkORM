#!/usr/bin/env python
"""
Quick way to get groupings of RethinkModels objects matching the given criteria
"""
import rethinkdb as r


class RethinkCollection(object):
    """
    A way to fetch groupings of documents that meet a criteria and have them
    in an iterable storage object, with each document represented by
    `RethinkModel` objects
    """
    documents = []
    table = ""
    _model = None
    _query = None
    _filter = {}
    _join = None
    _joinedField = None

    def __init__(self, model, filter=None):
        """
        Instantiates a new collection, using the given models table, and
        wrapping all documents with the given model.

        Filter can be a dictionary or lambda, similar to the filters for the
        RethinkDB drivers filters.
        """
        self._model = model
        self._query = r.table(self._model.table)

        if filter:
            self._filter = filter
            self._query = self._query.filter(self._filter)

    def joinOn(self, model, onIndex):
        """
        Performs an eqJoin on with the given model. The resulting join will be
        accessible through the models name.
        """
        return self._joinOnAsPriv(model, onIndex, model.__name__)

    def joinOnAs(self, model, onIndex, whatAs):
        """
        Like `joinOn` but allows setting the joined results name to access it
        from.

        Performs an eqJoin on with the given model. The resulting join will be
        accessible through the given name.
        """
        return self._joinOnAsPriv(model, onIndex, whatAs)

    def _joinOnAsPriv(self, model, onIndex, whatAs):
        """
        Private method for handling joins.
        """
        if self._join:
            raise Exception("Already joined with a table!")

        self._join = model
        self._joinedField = whatAs
        table = model.table
        self._query = self._query.eq_join(onIndex, r.table(table))
        return self

    def orderBy(self, field, direct="desc"):
        """
        Allows for the results to be ordered by a specific field. If given,
        direction can be set with passing an additional argument in the form
        of "asc" or "desc"
        """
        if direct == "desc":
            self._query = self._query.order_by(r.desc(field))
        else:
            self._query = self._query.order_by(r.asc(field))

        return self

    def __iter__(self):
        for doc in self._documents:
            yield doc

    # Pagination helpers...
    # These are questionable, on if I'll put them in or not.
    #def paginate(self, start,finish):
        #pass

    #@property
    #def currentPage(self):
        #pass

    #@property
    #def perpage(self):
        #pass

    #@property
    #def hasnextpage(self):
        #pass

    #@property
    #def pages(self):
        #pass
    # Okay, enough pagination

    def fetch(self):
        """
        Fetches the query and then tries to wrap the data in the model, joining
        as needed, if applicable.
        """
        returnResults = []

        results = self._query.run()
        for result in results:
            if self._join:
                # Because we can tell the models to ignore certian fields,
                # through the protectedItems blacklist, we can nest models by
                # name and have each one act normal and not accidentally store
                # extra data from other models
                item = self._model.fromRawEntry(**result["left"])
                joined = self._join.fromRawEntry(**result["right"])
                item.protectedItems = self._joinedField
                item[self._joinedField] = joined

            else:
                item = self._model.fromRawEntry(**result)

            returnResults.append(item)

        self._documents = returnResults
        return self._documents
