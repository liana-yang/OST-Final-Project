import logging

import ost_final_project.utility as utility
from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from ost_final_project.forms import CreateResourceForm, CreateReservationForm
from ost_final_project.models import Resource
from ost_final_project.views import HomePageView, CreateReservationView, ResourcePageView, \
    EditResourceView, TagPageView


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()
app.json_encoder = utility.NdbJSONEncoder


@app.route('/')
def render_home_page():
    view = HomePageView()
    return render_template('main.html', view=view)


@app.route('/resource/<resource_id>')
def render_resource(resource_id):
    view = ResourcePageView(resource_id)
    return render_template('resource.html', view=view)


@app.route('/tag/<tag_id>')
def render_tag(tag_id):
    view = TagPageView(tag_id)
    return render_template('tag.html', view=view)


@app.route('/create-resource', methods=['GET', 'POST'])
def render_create_resource():
    resource = Resource()
    view = EditResourceView(resource, 'Create A New Resource')
    form = CreateResourceForm(csrf_enabled=False)
    if form.validate_on_submit():
        resource = utility.update_resource_from_form(form, resource)
        resource.owner = view.user
        resource.put()
        resource_id = resource.key.id()
        return redirect(url_for('render_resource', resource_id=str(resource_id)))
    return render_template('edit_resource.html', view=view, form=form)


@app.route('/edit-resource/<resource_id>', methods=['GET', 'POST'])
def render_edit_resource(resource_id):
    resource = utility.get_resource_by_id(resource_id)
    view = EditResourceView(resource, 'Edit Resource: ' + resource.name)
    form = CreateResourceForm(csrf_enabled=False)
    if form.validate_on_submit():
        resource = utility.update_resource_from_form(form, resource)
        resource.put()
        return redirect(url_for('render_resource', resource_id=str(resource_id)))
    return render_template('edit_resource.html', view=view, form=form)


@app.route('/create-reservation/<resource_id>', methods=['GET', 'POST'])
def render_create_reservation(resource_id):
    view = CreateReservationView(resource_id)
    form = CreateReservationForm(csrf_enabled=False)
    form = utility.add_timerange_validators(form, resource_id)
    if form.validate_on_submit():
        reservation = utility.get_reservation_from_form(form)
        reservation.owner = view.user
        reservation.resource_key = utility.get_resource_key_by_id(resource_id)
        reservation.put()

        resource = view.resource
        resource.reservation_keys.append(reservation.key)
        resource.put()
        return redirect(url_for('render_home_page'))
    return render_template('create_reservation.html', view=view, form=form)


@app.route('/delete-reservation/<reservation_id>', methods=['GET', 'POST'])
def delete_reservation(reservation_id):
    reservation = utility.get_reservation_by_id(reservation_id)
    resource_key = reservation.resource_key
    resource = utility.get_resource_by_id(resource_key.id())
    reservation_idx = resource.reservation_keys.index(reservation.key)
    del resource.reservation_keys[reservation_idx]
    resource.put()
    reservation.key.delete()
    return redirect(url_for('render_home_page'))


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
