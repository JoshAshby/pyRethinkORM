#!/usr/bin/env python
"""
This module is a temporary module to demonstrate and provide a testing ground
for implimenting a relationship based system within the RethinkModel class.

>>> import rethinkdb as r
>>> import rethinkORM.rethinkRelation as rr
>>> conn = r.connect('localhost', 28015)
>>> a = r.db_create("model").run(conn)
>>> conn.use("model")
>>> conn.repl() #doctest: +ELLIPSIS
<rethinkdb.net.Connection ...>

>>> a = r.table_create("comments").run()
>>> a = r.table_create("posts").run()

>>> class Comment(rr.RethinkRelation):
...   table = "comments"

>>> class Post(rr.RethinkRelation):
...   table = "posts"
...   has_many = [Comment]

>>> p = Post.create(title="Rising", body="The city of Atlantis comes to life\
 as the special Stargate team arives in the gate room.") #doctest: +ELLIPSIS

>>> p #doctest: +ELLIPSIS
<RethinkRelation.Post ...>

>>> p.comments.create(author="O'Niell", comment="That's O'Niell, with two\
 l's!") #doctest: +ELLIPSIS
<RethinkRelation.comments ...>

>>> p.comments.all() #doctest: +ELLIPSIS
<RethinkCollection ...>

>>> a = r.db_drop("model").run()
"""
import rethinkModel as rm
import rethinkCollection as rc


class RethinkRelation(rm.RethinkModel):
  """
  Extension of the standard RethinkModel which allows for the creating of
  one to one and one to many relationships between documents. Eventually this
  will be merged into RethinkModel before the next release.

  Documents have a relation set through setting and storing of `foreign_key`
  which is simply the id of the parent document. This class takes care of
  setting and working with that key to ensure that things run smoothly.
  """

  #has_one = []
  has_many = []
  """
  Defines a relationship of one parent to many children documents

  Must be a list, and can be filled with classrefs for the models that
  this model has many of. The name of the property on the parent object will
  be the childs name, lowercased with an appended `s`
  """

  def finish_init(self):
    self._build_relationships()

  def _build_relationships(self):
    """
    Builds the relationships based off of the classrefs given in has_many and
    has_one.
    """
    self._set_keys_later = []
    def build_relation_class(wat, plural=False):
      data = {"foreign_key": self.id}
      if not plural:
        data.update({"unique": True})

      for obj in wat:
        name = obj.__name__.lower()
        if plural:
          name += "s"

        temp_class = type(name, (obj,), data)
        self._set(name, temp_class)
        self.protected_items = name
        self._set_keys_later.append(name)

    #if self.has_one is not None:
      #assert type(self.has_one) is list
      #build_relation_class(self.has_one)

    if self.has_many is not None:
      assert type(self.has_many) is list
      build_relation_class(self.has_many, True)

  def save(self):
    if hasattr(self, "foreign_key"):
      self._data["foreign_key"] = self.foreign_key

    #if hasattr(self, "unique"):
      #pass # TODO: Do some fancy, arcanie, black magic to make this remain unique

    super(RethinkRelation, self).save()

    for key in self._set_keys_later:
      self._get(key).foreign_key = self.id

  @classmethod
  def all(cls):
    """
    Returns a RethinkCollection which represents all of documents within this
    model, or all of the children if the model is attached to a parent through
    has_many.
    """
    if hasattr(cls, "foreign_key") and cls.foreign_key is not None:
      return rc.RethinkCollection(cls, {"foreign_key": cls.foreign_key})
    else:
      return rc.RethinkCollection(cls)

  @classmethod
  def find(cls, field, value):
    """
    Helper method to return a RethinkCollection with the given search.
    """
    return rc.RethinkCollection(cls, {field: value})

  def __repr__(self):
    """
    Allows for the representation of the object, for debugging purposes
    """
    return "<RethinkRelation.%s at %s with data: %s >" % (self.__class__.__name__,
                                           id(self),
                                           self._data)
