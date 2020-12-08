from flask_restful import Resource, request
from department_app.models.department import DepartmentModel, department_schema, departments_schema


class Department(Resource):
    """

    """
    def get(self, _id):
        """

        :param _id: integer
        :return: JSON
        """
        department = DepartmentModel.query.filter_by(id=_id).first()
        if department:
            department.update_average_salary()
            return department_schema.jsonify(department)
        return {'message': 'Department not found'}, 404

    def post(self):
        """

        :return:
        """
        json_data = request.get_json()
        if not json_data:
            return {'message': 'Please specify'}, 400
        data = json_data['name']
        department = DepartmentModel.find_by_name(data)

        if department:
            return {'message': 'Department already exists'}, 400
        new_department = DepartmentModel(data)
        new_department.insert()
        return department_schema.jsonify(new_department)

    def delete(self, _id):
        """

        :param _id:
        :return:
        """
        department = DepartmentModel.query.filter_by(id=_id).first()
        if department:
            department.remove()
            return {'message': 'Department deleted!'}
        return {'message': 'Department not found'}, 404

    def put(self, _id):
        """

        :param _id:
        :return:
        """
        department = DepartmentModel.query.filter_by(id=_id).first()
        if department:
            department.name = request.json['name']
            department.insert()
            return department_schema.jsonify(department)
        return {'message': 'Department not found'}, 404


class DepartmentList(Resource):
    """

    """
    def get(self):
        """
        Shows all departments
        :return: JSON
        """
        departments = DepartmentModel.query.all()
        for dep in departments:
            dep.count_employees()
            dep.update_average_salary()

        return departments_schema.jsonify(departments)
