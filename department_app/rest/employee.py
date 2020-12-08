from datetime import datetime
from flask_restful import Resource, request
from sqlalchemy import or_
from department_app.models.employee import EmployeeModel, employees_schema, employee_schema



class Employee(Resource):
    """

    """

    def get(self, _id):
        """
        Shows an employee as per given json values.
        If not found returns warning.

        :param _id: integer
        :param name: string
        :param dob: datetime
        :return: JSON
        """

        employee = EmployeeModel.find_by_id(_id)
        if employee:
            return employee_schema.jsonify(employee)

    def post(self):
        """
        Checks if employee with given json values exists.
        if not Creates a new user from the given json values
        else returns a message.

        :return: JSON
        """
        json_data = request.get_json()
        if not json_data:
            return {'message': 'Please specify'}, 400
        parsed_data = employee_schema.load(json_data)
        employee = EmployeeModel.check_identical(**parsed_data)
        if employee:
            return {'message': 'Employee already exists'}, 400
        employee = EmployeeModel(**parsed_data)
        employee.insert()
        return employee_schema.jsonify(employee)

    def delete(self, _id):
        """

        :param _id:
        :return:
        """
        employee = EmployeeModel.find_by_id(_id)
        if employee:
            if employee.department:
                employee.department.update_average_salary()
            employee.remove()
            return {'message': 'Employee deleted!'}
        return {'message': 'Employee not found'}

    def put(self, _id):
        """

        :param _id:
        :return:
        """
        employee = EmployeeModel.find_by_id(_id)
        if employee:
            data = request.get_json()
            parsed_data = employee_schema.load(data)
            if 'name' in parsed_data:
                employee.name = parsed_data['name']
            if 'salary' in parsed_data:
                employee.salary = parsed_data['salary']
            if 'dob' in parsed_data:
                employee.dob = parsed_data['dob']
            if 'department_id' in parsed_data:
                employee.department_id = parsed_data['department_id']

            employee.insert()
            #employee.department.update_average_salary()
            return employee_schema.jsonify(employee)
    # maybe create new object instead of msg
        return {'message': 'Employee not found'}


class EmployeeList(Resource):
    """
    Resource of ALL employees
    """
    def get(self):
        """
        Shows all employees
        :return:
        """
        # get parameters
        name = request.args.get('name')
        date1 = request.args.get('date1')
        date2 = request.args.get('date2')
        department = request.args.get('department')

        filtered_employees = EmployeeModel.query

        if len(request.args) == 0:
            return employees_schema.jsonify(filtered_employees.all())
        elif name or date1 or date2 or department:
            if date1 and date2:
                formatted_date1 = datetime.strptime(date1, "%Y-%m-%d")
                formatted_date2 = datetime.strptime(date2, "%Y-%m-%d")
                filtered_employees = EmployeeModel.query.filter(EmployeeModel.dob.between(formatted_date1,
                                                                                          formatted_date2))

            elif date1:
                formatted_date = datetime.strptime(date1, "%Y-%m-%d")
                filtered_employees = EmployeeModel.query.filter_by(dob=formatted_date)

            if name:
                # Implement search by ALIKE string if enough time
                filtered_employees = filtered_employees.filter_by(name=name)

            if department:
                print(department)
                if department == '0':
                    filtered_employees = filtered_employees.filter(EmployeeModel.department_id == None)
                else:
                    filtered_employees = filtered_employees.filter(EmployeeModel.department_id == department)

            return employees_schema.jsonify(filtered_employees.all())
        else:
            return {'message': 'Employee(s) not found'}, 404
