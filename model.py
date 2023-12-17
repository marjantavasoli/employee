from peewee import *
from prettytable import PrettyTable

db = SqliteDatabase("employee.sqlite")


class Employee(Model):
    first_name = TextField(null=False)
    last_name = TextField(null=False)
    birthday = DateField(formats=['%Y%m%d'], null=False)
    national_code = TextField(unique=True, null=False)

    class Meta:
        database = db
        db_table = "Employee"

# Employee.create_table()
    @staticmethod
    def get_all():
        '''
        :return:ModelSelect
        '''
        rows = Employee.select()

        db.close()
        return rows

    # @staticmethod
    # def search(**kwargs):
    #     rows = Employee.select().where()

    @staticmethod
    def add(first_name, last_name, birthday, national_code):
        employee = Employee(first_name=first_name, last_name=last_name, birthday=birthday, national_code=national_code)
        return employee.save()

    @staticmethod
    def search_national_code(national_code):
        employee = Employee.select().where(Employee.national_code == national_code)
        if employee:
            return employee

    @staticmethod
    def search_name(first_name):
        employee = Employee.select().where(Employee.first_name.contains(first_name))
        if employee:
            return employee

    @staticmethod
    def delete_by_national_code(national_code):
        if Employee.search_national_code(national_code=national_code):
            q = Employee.delete().where(Employee.national_code == national_code)
            q.execute()
            return True


Employee.create_table()
