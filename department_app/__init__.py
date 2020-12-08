import os

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from department_app.config import DevelopmentConfig
from department_app.db import db, ma
from department_app.rest.department import Department, DepartmentList
from department_app.rest.employee import Employee, EmployeeList
from department_app.models.department import *
from department_app.models.employee import *


# create and configure the app
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../db.sqlite')


with app.app_context():
    api = Api(app)
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)


    @app.before_first_request
    def create_db():
        with app.app_context():
            db.create_all()

    # API ROUTES
    api.add_resource(Department, '/api/department/<int:_id>')
    api.add_resource(Department, '/api/department/new', endpoint='post-department')
    api.add_resource(DepartmentList, '/api/departments/')
    api.add_resource(Employee, '/api/employee/<int:_id>', endpoint='single-employee')
    api.add_resource(Employee, '/api/employee/new', endpoint='post-employee')
    api.add_resource(EmployeeList, '/api/employees/')
    api.add_resource(EmployeeList, '/api/search/employees/', endpoint='filter')

    # VIEWS
    from . import views


# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass