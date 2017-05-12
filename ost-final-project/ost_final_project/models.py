from google.appengine.ext import ndb


class Reservation(ndb.Model):
    owner = ndb.StringProperty()  # Take user's nickname as unique ID.
    resource_key = ndb.KeyProperty('Resource')
    start_time = ndb.TimeProperty()
    end_time = ndb.TimeProperty()


class Tag(ndb.Model):
    name = ndb.StringProperty()


class Resource(ndb.Model):
    name = ndb.StringProperty()
    date = ndb.DateProperty()
    start_time = ndb.TimeProperty()
    end_time = ndb.TimeProperty()
    tags = ndb.StructuredProperty(Tag, repeated=True)
    owner = ndb.UserProperty()  # Take user's nickname as unique ID.
    reservations = ndb.StructuredProperty(Reservation, repeated=True)
