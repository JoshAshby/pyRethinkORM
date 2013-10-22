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
    def __init__(self, model, filter=None, query=None):
        """
        Instantiates a new collection, using the given models table, and
        wrapping all documents with the given model.

        Filter can be a dictionary of keys to filter by, a lambda or a similar
        statement, see:
        `RethinkDB Filters <http://www.rethinkdb.com/api/#py:selecting_data-filter>`__
        for more information

        A pre built query can also be passed in, to allow for better control
        of what documents get included in the final collection.

        :param model: A RethinkModel object to be used to wrap all documents in
        :param filter: If provided, it will be passed using the ReQL .filter command
        :param query: An optional pre built ReQL query to be used
        """
        self._documents = []
        self._filter = {}
        self._model = model

        if query:
            self._query = query
        else:
            self._query = r.table(self._model.table)

        if filter:
            self._filter = filter
            self._query = self._query.filter(self._filter)

    def order_by(self, key, direction="desc"):
        """
        Allows for the results to be ordered by a specific field. If given,
        direction can be set with passing an additional argument in the form
        of "asc" or "desc"

        :param key: The key to sort by
        :param direction: The direction, DESC or ASC to sort by
        """
        if direction.lower() == "desc":
            self._query = self._query.order_by(r.desc(key))
        else:
            self._query = self._query.order_by(r.asc(key))

        return self

    def limit(self, limit, offset=0):
        """
        Limits the results to the given offset (0 if not given) and the stated
        limit.

        :param limit: The number of documents that the results should be limited to
        :param offset: The number of documents to skip
        """
        self._query = self._query.skip(offset).limit(limit)

    def filter(self, filters):
        """
        Allows for the addition of more filters to the results.

        Filter can be a dictionary of keys to filter by, a lambda or a similar
        statement, see:
        `RethinkDB Filters <http://www.rethinkdb.com/api/#py:selecting_data-filter>`__
        for more information
        """
        self._query = self._query.filter(filters)

    def __len__(self):
        return len(self._documents)

    def __iter__(self):
        for doc in self._documents:
            yield doc

    def __getitem__(self, index):
        assert isinstance(index, int)
        return self._documents[index]

    def fetch(self):
        """
        Fetches the query results and wraps the documents in the collections model.

        Documents can then be accessed through the standard collection[index]
        or with a for loop:

        for doc in collection:
            pass
        """
        returnResults = []

        results = self._query.run()
        for result in results:
            returnResults.append(self._model(**result))

        self._documents = returnResults
        return self._documents

    @property
    def documents(self):
        if self._documents:
            return self._documents
        else:
            return self.fetch()
