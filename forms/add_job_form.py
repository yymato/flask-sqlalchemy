from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.fields import EmailField
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField, HiddenField, StringField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):

    team_leader = SelectField('TeamLead', validators=[DataRequired()])
    job = TextAreaField('Description', validators=[DataRequired()])
    work_size = IntegerField('Work_size', validators=[DataRequired()])
    collaborators = SelectMultipleField('Collaborators')
    submit = SubmitField('Создать')

class EditJobForm(JobForm):
    job_id = StringField('job_id')