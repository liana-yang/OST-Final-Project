import utility
from models import Resource, Reservation


class HomePageView(object):
    def __init__(self):
        # TODO(Ling): Build log_info.
        self.logged_in, self.user, self.log_url, self.log_msg = utility.autheticate()
        self.all_resources = self.get_all_resources()
        self.my_resources = self.get_my_resources()
        self.my_reservations = self.get_my_reservations()

        self.all_resources_table_view = ResourceTableView(self.all_resources, 'All Resources')
        self.my_resources_table_view = ResourceTableView(self.my_resources, 'My Resources')
        self.my_reservations_table_view = ReservationTableView(self.my_reservations, 'My Reservations')

    def get_all_resources(self):
        # TODO(Ling): Implement multiple pages.
        data = Resource.query().fetch(20)
        return data

    def get_my_resources(self):
        # TODO(Ling): Implement multiple pages.
        data = Resource.query(Resource.owner == self.user).fetch(20)
        return data

    def get_my_reservations(self):
        # TODO(Ling): Implement multiple pages.
        data = Reservation.query(Reservation.owner == self.user).fetch(20)
        return data


class ResourceTableView(object):
    def __init__(self, resources, title=''):
        self.title = title
        self.resources = self.resources_wrapper(resources)

    def resources_wrapper(self, resources):
        data = []
        for resource in resources:
            data.append(ResourceWrapper(resource))
        return data


class ReservationTableView(object):
    def __init__(self, reservations, title=''):
        self.title = title
        self.reservations = self.reservations_wrapper(reservations)

    def reservations_wrapper(self, reservations):
        data = []
        for reservation in reservations:
            data.append(ReservationWrapper(reservation))
        return utility.filter_by_current_datetime(data)


class EditResourceView(object):
    def __init__(self, resource, title):
        # TODO(Ling): Build log_info.
        self.logged_in, self.user, self.log_url, self.log_msg = utility.autheticate()
        self.resource = ResourceWrapper(resource)
        self.tags_str = self.get_tags_str()

        self.title = title

    def get_tags_str(self):
        tags_array = []
        for tag in self.resource.tags:
            tags_array.append(tag.name)
        return ','.join(tags_array)


class CreateReservationView(object):
    def __init__(self, resource_id):
        # TODO(Ling): Build log_info.
        self.logged_in, self.user, self.log_url, self.log_msg = utility.autheticate()
        self.resource_id = resource_id
        self.resource = ResourceWrapper(utility.get_resource_by_id(self.resource_id))

        self.title = "Create Reservation: " + self.resource.name


class ResourcePageView(object):
    def __init__(self, resource_id):
        # TODO(Ling): Build log_info.
        self.logged_in, self.user, self.log_url, self.log_msg = utility.autheticate()
        self.resource_id = resource_id
        self.resource = utility.get_resource_by_id(self.resource_id)
        self.resource_table_view = ResourceTableView([self.resource], 'Resource: ' + self.resource.name)


class ReservationWrapper(object):
    def __init__(self, reservation):
        self.model = reservation
        self.key = reservation.key
        self.owner = reservation.owner
        self.start_time = reservation.start_time
        self.end_time = reservation.end_time
        self.resource = self.get_resource()

    # TODO(Ling): Get the entity by key.
    def get_resource(self):
        return utility.get_resource_by_id(self.model.resource_key.id())


class ResourceWrapper(object):
    def __init__(self, resource):
        self.model = resource
        self.key = resource.key
        self.name = resource.name
        self.date = resource.date
        self.start_time = resource.start_time
        self.end_time = resource.end_time
        self.owner = resource.owner
        self.tags = self.tags_wrapper()
        self.reservations = self.reservations_wrapper()

    # TODO(Ling): Build an utility function.
    def tags_wrapper(self):
        tags = []
        for tag_key in self.model.tag_keys:
            tag = utility.get_tag_by_id(tag_key.id())
            tags.append(tag)
        return tags

    def reservations_wrapper(self):
        reservations = []
        for reservation_key in self.model.reservation_keys:
            reservation = utility.get_reservation_by_id(reservation_key.id())
            reservations.append(ReservationWrapper(reservation))
        return reservations
