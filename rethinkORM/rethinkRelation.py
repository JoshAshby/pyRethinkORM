import rethinkdb as r
import rethinkModel as rm
import rethinkCollection as rc


class RethinkRelation(rm.RethinkModel):
  has_one = []
  has_many = []

  def finish_init(self):
    self.relationships()

  def relationships(self):
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

    if self.has_one is not None:
      assert type(self.has_one) is list
      build_relation_class(self.has_one)

    if self.has_many is not None:
      assert type(self.has_many) is list
      build_relation_class(self.has_many, True)

  def save(self):
    if hasattr(self, "foreign_key"):
      self._data["foreign_key"] = self.foreign_key

    if hasattr(self, "unique"):
      pass # TODO: Do some fancy, arcanie, black magic to make this remain unique

    super(RethinkRelation, self).save()

    for key in self._set_keys_later:
      self._get(key).foreign_key = self.id


  @classmethod
  def all(cls):
    if hasattr(cls, "foreign_key") and cls.foreign_key is not None:
      return rc.RethinkCollection(cls, {"foreign_key": cls.foreign_key})
    else:
      return rc.RethinkCollection(cls)

  @classmethod
  def find(cls, field, value):
      query = r.table(cls.table).filter({field: value}).coerce_to('array').run()
      return query
