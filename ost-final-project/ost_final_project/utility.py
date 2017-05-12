import json
from datetime import datetime, date, time

from google.appengine.api import users
from google.appengine.ext import ndb

from flask.json import JSONEncoder
from models import Resource, Reservation
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
    resource.tags = [Tag(name="data.tags")]
    return resource


def get_reservation_from_form(form):
    return Reservation(start_time=form.start_time.data, end_time=form.end_time.data)


def get_resource_by_id(resource_id):
    return Resource.get_by_id(int(resource_id))


def get_reservation_by_id(reservation_id):
    return Reservation.get_by_id(int(reservation_id))


def get_resource_key_by_id(resource_id):
    return ndb.Key(Resource, int(resource_id))


def get_reservation_key_by_id(reservation_id):
    return ndb.Key(Reservation, int(reservation_id))


def filter_by_current_datetime(reservation_views):
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    valid_reservation_views = []
    for reservation_view in reservation_views:
        resource = reservation_view.resource
        if resource.date < current_date:
            continue
        if reservation_view.end_time <= current_time:
            continue
        valid_reservation_views.append(reservation_view)
    return valid_reservation_views


def add_timerange_validators(form, resource_id):
    resource = get_resource_by_id(resource_id)
    form.start_time.validators.append(TimeRange(min=resource.start_time))
    form.end_time.validators.append(TimeRange(max=resource.end_time))
    return form


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
