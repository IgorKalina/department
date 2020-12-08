from department_app.service.db import db, ma


class DepartmentModel(db.Model):

    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    average_salary = db.Column(db.Float(precision=2))
    employees = db.relationship('EmployeeModel', backref='department')
    num_of_employees = 0

    def __init__(self, name, average_salary=0):
        self.name = name
        self.average_salary = average_salary
        self.num_of_employees = 0

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    # average_salary_calculation
    def update_average_salary(self):
        total = 0
        for i in self.employees:
            total += float(i.salary)
        try:
            self.average_salary = round(total / len(self.employees), 2)
        except ZeroDivisionError:
            self.average_salary = 0

    def count_employees(self):
        self.num_of_employees = len(self.employees)


class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'average_salary', 'num_of_employees')


department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

