class Person:
    def __init__(self, name):
        self.name = name
    def get_name(self):
        return self.name

class Employee(Person):
    def __init__(self, name, emp_id):
        super().__init__(name)
        self.emp_id = emp_id
    def get_emp_id(self):
        print(f'emp id {self.emp_id}')

class Admin(Person):
    def __init__(self, name, admin_id):
        super().__init__(name)
        self.admin_id = admin_id
    def get_emp_id(self):
        print(f'admin id {self.admin_id}')

from abc import ABC, abstractmethod
class Factory:
    @abstractmethod
    def create_obj(self, name, id):
        pass

class EmployeeFactory(Factory):
    def create_obj(self, name, id):
        return Employee(name, id)

class AdminFactory(Factory):
    def create_obj(self, name, id):
        return Admin(name, id)

factory = EmployeeFactory()
e = factory.create_obj(1, 1)

factory = AdminFactory()
a = factory.create_obj(100, 100)

e.get_emp_id()
a.get_emp_id()