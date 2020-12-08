from tests.conftests import _app
from flask import redirect, url_for
EMP_VIEW_URL = '/employee'
DEP_VIEW_URL = '/department'
DEP_API_URL = '/api/department/'
EMP_API_URL = '/api/employee/'


def test_home(_app):
    response = _app.get('/')
    assert response.status_code == 200


def test_all_employees(_app):
    response = _app.get(EMP_VIEW_URL + 's')
    assert response.status_code == 200


def test_all_departments(_app):
    response = _app.get(DEP_VIEW_URL + 's')
    response_post = _app.post(DEP_API_URL + 'new', json={'name': 'TEST1'})
    response_empty_post = _app.post(DEP_API_URL + 'new')
    assert response.status_code == 200
    assert response_post.status_code == 200
    assert response_post.get_json() == {
        "average_salary": 0.0,
        "id": 2,
        "name": "TEST1",
        "num_of_employees": 0
    }
    assert response_empty_post.status_code == 400
    assert redirect(url_for('display_departments')).location == DEP_VIEW_URL + 's'


def test_single_employee(_app):
    response_p = _app.get(EMP_VIEW_URL + '/1')
    response_m = _app.get(EMP_VIEW_URL + '/22')

    assert response_p.status_code == 200
    assert response_m.status_code == 200




def test_single_department(_app):
    response_p = _app.get(DEP_VIEW_URL + '/1')
    response_m = _app.get(DEP_VIEW_URL + '/2')
    response_empl_p = _app.get('/api/search/employees/?&department=1')
    response_empl_m = _app.get('/api/search/employees/?&department=2')
    assert response_p.status_code == 200
    assert response_m.status_code == 200
    assert response_empl_p.status_code == 200
    assert response_empl_m.status_code == 200
    assert response_empl_m.get_json() == []


def test_create_employee(_app):
    response = _app.get('/new' + EMP_VIEW_URL + '/')
    assert response.status_code == 200

