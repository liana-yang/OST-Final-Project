from models import Resource, Tag
from flask.json import JSONEncoder
from google.appengine.ext import ndb
import json, datetime
from datetime import date, time
from models import Resource, Reservation


def get_resource_from_form(form):
    return Resource(name=form.name.data, date=form.date.data, start_time=form.start_time.data,
                    end_time=form.end_time.data,
                    tags=[Tag(name="data.tags")])


def get_reservation_from_form(form):
    return Reservation(start_time=form.start_time.data, end_time=form.end_time.data)


def get_resource_by_id(resource_id):
    return Resource.get_by_id(int(resource_id))


def get_reservation_by_id(reservation_id):
    return Reservation.get_by_id(int(reservation_id))


def get_resource_key_by_id(resource_id):
    return ndb.Key(Resource, resource_id)


class NdbJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ndb.Model):
            new = self.to_json(obj.to_dict())
            return json.dumps(new)
        return JSONEncoder.default(self, obj)

    def to_json(self, obj):
        if isinstance(obj, dict):
            new_dict = {}
            # new_dict['id'] = obj['key'].id()
            for item in obj:
                new_dict[item] = self.to_json(obj[item])
            return new_dict
        # elif isinstance(obj, ndb.Key):
        #     return obj.urlsafe()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, time):
            return obj.isoformat()
        return obj
