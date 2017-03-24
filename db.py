from google.appengine.ext import ndb


class Post(ndb.Model):
    text = ndb.StringProperty()
    fb_id = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

