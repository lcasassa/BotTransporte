from google.appengine.ext import ndb


class Post(ndb.Model):
    text = ndb.StringProperty()
    fb_id = ndb.StringProperty()
    date = ndb.DateTimeProperty(indexed = True)
    username = ndb.StringProperty()
    user_id = ndb.StringProperty()
    url = ndb.StringProperty()

class LastPostSent(ndb.Model):
    #chat_id = ndb.StringProperty() #using id as chat_id
    date = ndb.DateTimeProperty()

