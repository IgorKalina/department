from flask import render_template, request, redirect, url_for
import requests
from flask_bootstrap import Bootstrap

from department_app import app

from department_app.forms import (EmployeeCreateForm, DepartmentCreateForm,
                                  DepartmentEditForm, EmployeeEditForm, EmployeeSearchForm)
from werkzeug.datastructures import MultiDict

bootstrap = Bootstrap(app)

BASE_URL = 'http://127.0.0.1:5000'


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/departments', methods=['GET', 'POST'])
def display_departments():
    departments = requests.get(BASE_URL + '/api/departments/').json()
    employees = requests.get(BASE_URL + '/api/employees/').json()
    form = DepartmentCreateForm()
    if request.method == 'POST':
        payload = {'name': request.form.get('name')}
        requests.post(BASE_URL + '/api/department/new', json=payload)
        return redirect(url_for('display_departments'))

    return render_template('departments.html', departments=departments, employees=employees, form=form)


# ALL
@app.route('/employees', methods=['GET', 'POST'])
def display_employees():
    employees = requests.get(BASE_URL + '/api/employees/').json()
    departments = requests.get(BASE_URL + '/api/departments/').json()
    filtered = []
    # search-form
    select_choices = [('', '--select field--'), (0, 'No department')] + [(dep['id'], dep['name']) for dep in
                                                                         departments]
    # set default values
    form = EmployeeSearchForm()
    form.department.choices = select_choices

    if request.method == 'POST':
        request_url = BASE_URL + '/api/search/employees/?'
        if request.form.get('name'):
            request_url += 'name=' + request.form.get('name')
        if request.form.get('date1'):
            request_url += '&date1=' + request.form.get('date1')
        if request.form.get('date2'):
            request_url += '&date2=' + request.form.get('date2')
        if request.form.get('department'):
            request_url += '&department=' + request.form.get('department')
        response = requests.get(request_url)
        if response.status_code != 404 and hasattr(response, "__iter__"):
            filtered = response.json()
        else:
            filtered = response
    return render_template('employees.html', employees=employees, filtered=filtered, form=form, departments=departments)


# SINGLE
@app.route('/department/<_id>', methods=['GET', 'POST'])
def display_single_department(_id):
    req = requests.get(BASE_URL + '/api/department/' + _id)
    department = req.json()
    if req.status_code != 200:
        return department
    req_e = requests.get(BASE_URL + '/api/search/employees/?&department=' + str(department['id']))
    if req_e.status_code == 404:
        employees = req_e
    else:
        employees = req_e.json()
    form = DepartmentEditForm()
    if request.method == 'POST':
        payload = {'name': request.form.get('name')}
        requests.put(BASE_URL + '/api/department/' + _id, json=payload)
        return redirect(url_for('display_single_department', _id=_id))
        # maybe to make a redirect to a new object page

    return render_template('department.html', department=department, employees=employees, form=form)


# SINGLE
@app.route('/employee/<_id>', methods=['GET', 'POST'])
def display_single_employee(_id):
    req = requests.get(BASE_URL + '/api/employee/' + _id)
    employee = req.json()
    if req.status_code == 404:
        return employee
    employee = req.json()
    departments = requests.get(BASE_URL + '/api/departments/').json()
    select_choices = [(0, 'Not chosen')] + [(dep['id'], dep['name']) for dep in departments]

    # set default values
    form = EmployeeEditForm(formdata=MultiDict(employee))
    form.department.choices = select_choices
    # default for select field
    form.department.data = employee['department_id']
    # EDIT-FORM
    if request.method == 'POST':
        department_id = request.form.get('department')
        payload = {'name': request.form.get('name'),
                   'salary': request.form.get('salary'),
                   'dob': request.form.get('dob'),
                   'department_id': None if department_id == '0' else department_id}

        requests.put(BASE_URL + '/api/employee/' + _id, json=payload)
        return redirect(url_for('display_employees'))

    return render_template('employee.html', employee=employee, form=form, departments=departments)


@app.route('/new/employee/', methods=['GET', 'POST'])
def create_employee():
    employees = requests.get(BASE_URL + '/api/employees/').json()
    departments = requests.get(BASE_URL + '/api/departments/').json()
    # form-create
    form = EmployeeCreateForm()
    select_choices = [(0, 'Not chosen')] + [(dep['id'], dep['name']) for dep in departments]
    form.department.choices = select_choices

    if request.method == 'POST':
        department_id = request.form.get('department_id')
        payload = {'name': request.form.get('name'),
                   'salary': request.form.get('salary'),
                   'dob': request.form.get('dob'),
                   'department_id': None if department_id == 0 else department_id}

        requests.post(BASE_URL + '/api/employee/new', json=payload)
        return redirect(url_for('display_employees'))

    return render_template('create_employee.html', employees=employees, departments=departments, form=form)
