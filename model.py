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
        rows = Employee.select()
        # for row in rows:
        #     print("first_name: {} last_name: {} birthday: {} national_code:{}".format(row.first_name, row.last_name,
        #                                                                               row.birthday,
        #                                                                               row.national_code))
        db.close()
        return rows

    @staticmethod
    def search(**kwargs):
        rows = Employee.select().where()

    @staticmethod
    def add(first_name, last_name, birthday, national_code):
        empolyee = Employee(first_name=first_name, last_name=last_name, birthday=birthday, national_code= national_code)
        return empolyee.save()
