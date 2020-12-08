from department_app.service.db import db, ma
from marshmallow import fields


class EmployeeModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    salary = db.Column(db.Float(precision=2), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)

    def __init__(self, name, dob, salary, department_id=None):
        self.name = name
        self.dob = dob
        self.salary = salary
        self.department_id = department_id

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get_or_404(_id)

    @classmethod
    def check_identical(cls, name, dob, salary, department_id=None):
        return cls.query.filter_by(name=name, dob=dob, salary=salary, department_id=department_id).first()

    def insert(self):
        db.session.add(self)
        db.session.commit()
        if self.department:
            self.department.update_average_salary()
            db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()


class EmployeeSchema(ma.Schema):
    dob = fields.DateTime('%Y-%m-%d')
    department_id = fields.Field(allow_none=True)

    class Meta:
        fields = ('id', 'name', 'dob', 'salary', 'department_id')


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
