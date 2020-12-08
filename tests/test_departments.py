import pytest
from tests.conftests import _app
from department_app.models.department import DepartmentModel
DEP_API_URL = '/api/department/'
EMP_API_URL = '/api/employee/'


def test_department_model(_app):
    """ testing method of average salary"""
    # first delete default employee
    response_p = _app.delete(EMP_API_URL + '1')

    cur_dep = DepartmentModel.query.filter_by(id=1).first()
    total = 0
    for emp in cur_dep.employees:
        total += float(emp.salary)

    with pytest.raises(ZeroDivisionError):
        assert round(total / len(cur_dep.employees), 2)

    cur_dep.update_average_salary()
    assert response_p.status_code == 200
    assert cur_dep.average_salary == 0



def test_department_get(_app):
    """
    GIVEN a url
    WHEN id is passed
    THEN check response from server
    results:
    - id not in db(return not found)
    - id found(return json)
    - 'name' in response json
    """

    url_present_object = DEP_API_URL + '1'
    url_missing_object = DEP_API_URL + '2'

    response_p = _app.get(url_present_object)
    response_m = _app.get(url_missing_object)

    assert response_p.status_code == 200
    assert response_m.status_code == 404
    assert 'name' in response_p.get_json()


def test_department_post(_app):
    """
    GIVEN a url
    WHEN json with 'name'
    THEN check response from server

    results:
    if NEW name return JSON
    if existing name return message
    """

    data_present = {'name': 'Crewing'}
    data_missing = {'name': 'TEST'}

    # check if data in test BD
    response_e = _app.post(DEP_API_URL + 'new')
    response_p = _app.post(DEP_API_URL + 'new', json=data_present)
    response_m = _app.post(DEP_API_URL + 'new', json=data_missing)

    json_data = response_m.get_json()

    assert response_e.status_code == 400
    assert response_p.status_code == 400
    assert json_data == {
        "average_salary": 0.0,
        "id": 2,
        "name": "TEST",
        "num_of_employees": 0
    }
    assert response_m.status_code == 200



def test_department_put(_app):
    """
    GIVEN a url
    WHEN json with 'name'
    THEN check response from server

    results:
    if NEW name return JSON
    if existing name return message
    """

    data_missing = {'name': 'NO'}
    data_to_apply = {'name': 'TEST2'}

    # check if data in test BD
    response_m = _app.put(DEP_API_URL + '2', json=data_missing)
    response_p = _app.put(DEP_API_URL + '1', json=data_to_apply)

    json_data = response_p.get_json()

    assert response_m.status_code == 404
    assert json_data == {
        "average_salary": 0.0,
        "id": 1,
        "name": "TEST2",
        "num_of_employees": 0
    }
    assert json_data['name'] == data_to_apply['name']

#
def test_department_delete(_app):
    """
        GIVEN a url
        WHEN id is passed
        THEN check response from server
        if it is deleted or exists

        results:
        if existing name then delete
        if not then not found
        """
    url_present_object = DEP_API_URL + '1'
    url_missing_object = DEP_API_URL + '100'
    # check if data in test BD
    response_p = _app.delete(url_present_object)
    response_m = _app.delete(url_missing_object)

    assert response_p.get_json() == {'message': 'Department deleted!'}
    assert response_p.status_code == 200
    # check if ITEM not in database
    assert response_m.status_code == 404
#
#
def test_departments(_app):
        """
        GIVEN a url
        WHEN id is passed
        THEN check response from server
        if it is deleted or exists

        results:
        if existing name then delete
        if not then not found
        """

        url_plural = '/api/departments/'

        response = _app.get(url_plural)

        assert response.status_code == 200

