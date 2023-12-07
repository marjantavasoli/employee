from peewee import *
from prettytable import PrettyTable

db = SqliteDatabase("employee.sqlite")


class Employee(Model):
    first_name = TextField()
    last_name = TextField()
    birthday = DateField(formats=['%Y%m%d'])
    national_code = TextField(unique=True, null=False)

    class Meta:
        database = db
        db_table = "Employee"

# Employee.create_table()
    @staticmethod
    def show():
        rows = Employee.select()
        for row in rows:
            print("first_name: {} last_name: {} birthday: {} national_code:{}".format(row.first_name, row.last_name,
                                                                                      row.birthday,
                                                                                      row.national_code))
        db.close()

    @staticmethod
    def search(**kwargs):
        rows = Employee.select().where()