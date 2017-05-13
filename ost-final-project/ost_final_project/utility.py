import json
from datetime import datetime, date, time

from google.appengine.api import users
from google.appengine.ext import ndb

from flask.json import JSONEncoder
from models import Resource, Reservation, Tag
from models import Tag
from wtforms_components import TimeRange


def autheticate():
    user = users.get_current_user()
    if user:
        logged_in = True
        log_url = users.create_logout_url('/')
        log_msg = "Sign out"
    else:
        logged_in = False
        log_url = users.create_login_url('/')
        log_msg = "Sign in"
    return logged_in, user, log_url, log_msg


def update_resource_from_form(form, resource):
    resource.name = form.name.data
    resource.date = form.date.data
    resource.start_time = form.start_time.data
    resource.end_time = form.end_time.data
    tag_keys = []
    for tag_str in form.tags.data.split(","):
        tag = tag_exists(tag_str)
        if tag is None:
            tag = Tag(name=tag_str)
            tag.put()
        tag_keys.append(tag.key)
    resource.tag_keys = tag_keys
    return resource


def get_reservation_from_form(form):
    return Reservation(start_time=form.start_time.data, end_time=form.end_time.data)


def get_resource_by_id(resource_id):
    return Resource.get_by_id(int(resource_id))


def get_reservation_by_id(reservation_id):
    return Reservation.get_by_id(int(reservation_id))


def get_tag_by_id(tag_id):
    return Tag.get_by_id(int(tag_id))


def get_resource_key_by_id(resource_id):
    return ndb.Key(Resource, int(resource_id))


def get_reservation_key_by_id(reservation_id):
    return ndb.Key(Reservation, int(reservation_id))


def filter_by_current_datetime(reservations):
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    valid_reservations = []
    for reservation in reservations:
        resource = reservation.resource
        if resource.date < current_date:
            continue
        if reservation.end_time <= current_time:
            continue
        valid_reservations.append(reservation)
    return valid_reservations


def add_timerange_validators(form, resource_id):
    resource = get_resource_by_id(resource_id)
    form.start_time.validators.append(TimeRange(min=resource.start_time))
    form.end_time.validators.append(TimeRange(max=resource.end_time))
    return form


def tag_exists(tag_str):
    tag = Tag.query(Tag.name == tag_str).get()
    return tag


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
