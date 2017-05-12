from flask_wtf import FlaskForm
from wtforms import StringField, TextField
from wtforms_components import DateField, TimeField
from wtforms.validators import DataRequired

class CreateResourceForm(FlaskForm):
    # name = StringField('Resource Name', validators=[DataRequired()])
    name = StringField('Resource Name')
    date = DateField('Available Date')
    start_time = TimeField('Start time')
    end_time = TimeField('End time')
    tags = StringField('Tags')


class CreateReservationForm(FlaskForm):
    start_time = TimeField('Start time')
    end_time = TimeField('End time')
