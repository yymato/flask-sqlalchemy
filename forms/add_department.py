from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import HiddenField, TextAreaField, BooleanField, SubmitField, StringField, EmailField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    form_type = HiddenField(default="add")
    chief = SelectField('chief', validators=[DataRequired()])
    title = TextAreaField('title', validators=[DataRequired()])
    members = SelectMultipleField('members')
    email = EmailField('email', validators=[DataRequired()])
    submit = SubmitField('Создать')

class EditDepartmentForm(FlaskForm):
    form_type = HiddenField(default="edit")
    department_id = HiddenField(default=None)
    chief = SelectField('chief', validators=[DataRequired()])
    title = TextAreaField('title', validators=[DataRequired()])
    members = SelectMultipleField('members')
    email = EmailField('email', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
