import rethinkdb as r
import rethinkORM.rethinkRelation as rr

conn = r.connect('localhost', 28015)
conn.use("model")
conn.repl()


class Comment(rr.RethinkRelation):
  table = "comments"


class Post(rr.RethinkRelation):
  table = "posts"
  has_many = [Comment]


p = Post.create(title="wat", post="You daft twat")
p.comments.create(author="who?", comment="O_o")
a = p.comments.new(author="Dr.", comment="o_O")
a.save()
b = p.comments.find("author", "who?")
c = p.comments.all()
