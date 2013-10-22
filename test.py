import rethinkdb as r
import rethinkORM.rethinkRelation as rr

conn = r.connect('localhost', 28015)
conn.use("model")
conn.repl()


class Comment(rr.RethinkRelation):
  table = "comments"


class Author(rr.RethinkRelation):
  table = "authors"


class Post(rr.RethinkRelation):
  table = "posts"
  has_many = [Comment]
  has_one = [Author]


p = Post.create(title="wat", post="You daft twat")
a = p.comments.all()
p.comments.create(author="who?", comment="O_o")
b = p.comments.new(author="Dr.", comment="o_O")
b.save() # okay, because its a has_many, so another comment is created
c = p.comments.find("author", "who?")

p.author.create(name="Josh")

d = p.author.new(name="Fred")
d.save() # Should either fail and raise an exception,
         #   or save over the already created author,
         #   because of has_one? in which case how is
         #   this implimented because new/save/create
         #   is implimented by the Author comment and
         #   not the Post class.
