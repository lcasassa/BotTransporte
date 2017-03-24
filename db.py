from google.appengine.ext import ndb


class Post(ndb.Model):
    text = ndb.StringProperty()
    fb_id = ndb.StringProperty()
    date = ndb.DateTimeProperty()

class LastPostSent(ndb.Model):
    #chat_id = ndb.StringProperty() #using id as chat_id
    date = ndb.DateTimeProperty()

