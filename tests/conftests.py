import os
import tempfile
import pytest
import datetime


from department_app.config import TestingConfig
from department_app.models.department import DepartmentModel
from department_app.models.employee import EmployeeModel
from flask import Flask

#os.environ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
from department_app import app
from department_app import db as _db


@pytest.yield_fixture(scope='function')
def _app():
    """An application for the tests."""
    app.config.from_object(TestingConfig)

    with app.app_context():
        _db.create_all()
        new_dep = DepartmentModel(name='Crewing')
        new_emp = EmployeeModel(
            department_id=1,
            dob=datetime.datetime.strptime("2020-12-12", '%Y-%m-%d'),
            name="TEST0",
            salary=1000.0
        )
        _db.session.add(new_dep)
        _db.session.add(new_emp)
        _db.session.commit()

    ctx = app.test_request_context()
    ctx.push()

    yield app.test_client()

    _db.session.close()
    _db.drop_all()
    ctx.pop()




