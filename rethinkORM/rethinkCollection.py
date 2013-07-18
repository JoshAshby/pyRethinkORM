#!/usr/bin/env python
"""
Quick way to get groupings of RethinkModels objects matching the given criteria
"""
import rethinkdb as r
#from rethinkModel import RethinkModel


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
            self._query.filter(self._filter)

    def join(self, model, onIndex):
        """
        Performs an eqJoin on with the given model. The resulting join will be
        accessible through the models name.
        """
        if self._join:
            raise Exception("Already joined with a table!")

        self._join = model
        table = model.table
        self._query.eqJoin(onIndex, r.table(table))
        return self

    def orderBy(self, field):
        self._query.orderBy(field)
        return self

    def __repr__(self):
        pass

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
        returnResults = []

        results = self._query.run()
        for result in results:
            if self._join:
                pass
            print result
            #item = self._model(**result)

            #returnResults.append(item)

        return returnResults
