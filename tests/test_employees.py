from tests.conftests import _app
import json
from datetime import datetime

EMP_API_URL = '/api/employee/'


def test_employee_get(_app):
    url_present_object = EMP_API_URL + '1'
    url_missing_object = EMP_API_URL + '2'

    response_p = _app.get(url_present_object)
    response_m = _app.get(url_missing_object)

    assert response_p.status_code == 200
    assert response_m.status_code == 404
    assert 'name' in response_p.get_json()



def test_employee_post(_app):

    data_present = {
        "department_id": 1,
        "dob": "2020-12-12",
        "name": "TEST0",
        "salary": 1000.0
    }

    data_missing = {
        "department_id": 2,
        "dob": "2020-01-01",
        "name": "TEST1",
        "salary": 1500.0
    }

    response_e = _app.post(EMP_API_URL + 'new')
    response_p = _app.post(EMP_API_URL + 'new', json=data_present)
    response_m = _app.post(EMP_API_URL + 'new', json=data_missing)

    json_data = response_m.get_json()
    json_required = {
        "department_id": 2,
        "dob": "2020-01-01",
        "id": 2,
        "name": "TEST1",
        "salary": 1500.0
    }

    assert response_e.status_code == 400
    assert response_p.status_code == 400
    assert json_data == json_required
    assert response_m.status_code == 200


def test_employee_put(_app):
    data_missing = {
        "department_id": 2,
        "dob": "2020-01-01",
        "name": "TEST1",
        "salary": 1500.0
    }

    data_to_apply = {
        "department_id": 1,
        "dob": "2020-01-01",
        "name": "TEST2",
        "salary": 1500.0
    }

    # check if data in test BD
    response_m = _app.put(EMP_API_URL + '2', json=data_missing)
    response_p = _app.put(EMP_API_URL + '1', json=data_to_apply)

    json_data = response_p.get_json()

    assert response_m.status_code == 404
    assert json_data == {
        "department_id": 1,
        "dob": "2020-01-01",
        "id": 1,
        "name": "TEST2",
        "salary": 1500.0
    }
    assert json_data['name'] == data_to_apply['name']


def test_employee_delete(_app):

    # check if data in test BD
    response_m = _app.delete(EMP_API_URL + '2')
    response_p = _app.delete(EMP_API_URL + '1')

    assert response_m.status_code == 404
    assert response_p.status_code == 200
    assert response_p.get_json() == {'message': 'Employee deleted!'}


def test_employees(_app):
    url = '/api/employees/'
    url_filter = url + '?'
    name = 'name=Albert Mayer'
    single_date = "&date1=2020-12-23"
    double_date = "&date1=2020-12-01&date2=2020-12-30"
    formatted_date1 = datetime.strptime('2020-12-01', "%Y-%m-%d")
    formatted_date2 = datetime.strptime('2020-12-30', "%Y-%m-%d")
    department = "&department=0"
    all_one_date = name + single_date + department
    all_two_dates = name + double_date + department
    nonsense = 'XDXDXDXDXD'

    response_bare = _app.get(url)
    response_name = _app.get(url_filter + name)
    response_single_date = _app.get(url_filter + single_date)
    response_double_date = _app.get(url_filter + double_date)
    response_department = _app.get(url_filter + department)
    response_all_one_date = _app.get(url_filter + all_one_date)
    response_all_two_dates = _app.get(url_filter + all_two_dates)
    response_nonsense = _app.get(url_filter + nonsense)

    assert response_bare.get_json() == [
        {
            "department_id": 1,
            "dob": "2020-12-12",
            "id": 1,
            "name": "TEST0",
            "salary": 1000.0
        }
    ]
    for employee in response_name.get_json():
        assert employee['name'] == 'Albert Mayer'
    for employee in response_single_date.get_json():
        assert employee['dob'] == '2020-12-23'
    for employee in response_double_date.get_json():
        res_date_formatted = datetime.strptime(employee['dob'], "%Y-%m-%d")
        assert formatted_date1 < res_date_formatted < formatted_date2
    for employee in response_department.get_json():
        assert employee['department_id'] == 0
    for employee in response_all_one_date.get_json():
        assert employee['name'] == 'Albert Mayer'
        assert employee['dob'] == '2020-12-23'
        assert employee['department_id'] == 0
    for employee in response_all_two_dates.get_json():
        assert employee['name'] == 'Albert Mayer'
        res_date_formatted = datetime.strptime(employee['dob'], "%Y-%m-%d")
        assert formatted_date1 < res_date_formatted < formatted_date2
        assert employee['department_id'] == 0
    assert response_nonsense.status_code == 404

