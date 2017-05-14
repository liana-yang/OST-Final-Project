from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms_components import DateField, TimeField


class CreateResourceForm(FlaskForm):
    name = StringField('Resource Name', validators=[DataRequired()])
    date = DateField('Available Date', validators=[DataRequired()])
    start_time = TimeField('Start time', validators=[DataRequired()])
    end_time = TimeField('End time', validators=[DataRequired()])
    tags = StringField('Tags')


class CreateReservationForm(FlaskForm):
    start_time = TimeField('Start time', validators=[DataRequired()])
    end_time = TimeField('End time', validators=[DataRequired()])
