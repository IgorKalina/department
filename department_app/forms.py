from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class EmployeeCreateForm(FlaskForm):
    name = StringField('Name', _name='name', validators=[DataRequired()])
    dob = DateField('Date of birth', _name='dob', format='%Y-%m-%d', validators=[DataRequired()])
    salary = FloatField('Salary', _name='salary', default=0, validators=[DataRequired()])
    department = SelectField('Department', _name='department_id', coerce=int)

    submit = SubmitField('Add')


class EmployeeEditForm(EmployeeCreateForm):
    submit = SubmitField('Edit')


class DepartmentCreateForm(FlaskForm):
    name = StringField('Name', _name='name', validators=[DataRequired()])
    submit = SubmitField('Add')


class DepartmentEditForm(DepartmentCreateForm):
    submit = SubmitField('Edit')


class EmployeeSearchForm(FlaskForm):
    name = StringField('Name', _name='name', default='')
    date1 = DateField('Date of birth / From', _name='date1', format='%Y-%m-%d', default='')
    date2 = DateField('To', _name='date2', format='%Y-%m-%d', default='')
    department = SelectField('Department', _name='department_id', coerce=str)
    submit = SubmitField('Search')

