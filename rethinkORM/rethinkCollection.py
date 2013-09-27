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
    _model = None
    _query = None
    _filter = {}

    def __init__(self, model, filter=None, query=None):
        """
        Instantiates a new collection, using the given models table, and
        wrapping all documents with the given model.

        Filter can be a dictionary or lambda, similar to the filters for the
        RethinkDB drivers filters.

        A pre built query can also be passed in, to allow for better control
        of what documents get included in the final collection.
        """
        self._model = model

        if query:
            self._query = query
        else:
            self._query = r.table(self._model.table)

        if filter:
            self._filter = filter
            self._query = self._query.filter(self._filter)

    def order_by(self, field, direct="desc"):
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

    def limit(self, limit, offset=0):
        """
        Limits the results to the given offset (0 if not given) and the stated
        limit.
        """
        self._query = self._query.limit(limit).skip(offset)

    def filter(self, filters):
        """
        Allows for the addition of more filters to the resuls.
        """
        self._query = self._query.filter(filters)

    def __len__(self):
        return len(self._documents)

    def __iter__(self):
        for doc in self._documents:
            yield doc

    def fetch(self):
        """
        Fetches the query and then tries to wrap the data in the model, joining
        as needed, if applicable.
        """
        returnResults = []

        results = self._query.run()
        for result in results:
            returnResults.append(self._model(**result))

        self._documents = returnResults
        return self._documents
