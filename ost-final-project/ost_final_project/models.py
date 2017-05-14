from google.appengine.ext import ndb


class Reservation(ndb.Model):
    owner = ndb.UserProperty()
    resource_key = ndb.KeyProperty('Resource')
    start_time = ndb.TimeProperty()
    end_time = ndb.TimeProperty()


class Tag(ndb.Model):
    name = ndb.StringProperty()
    # TODO(Ling): Add resource_keys in accelerate the search.


class Resource(ndb.Model):
    name = ndb.StringProperty()
    date = ndb.DateProperty()
    start_time = ndb.TimeProperty()
    end_time = ndb.TimeProperty()
    tag_keys = ndb.KeyProperty('Tag', repeated=True)
    owner = ndb.UserProperty()
    reservation_keys = ndb.KeyProperty('Reservation', repeated=True)
