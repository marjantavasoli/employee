from peewee import *
from prettytable import PrettyTable

db = SqliteDatabase("employee.sqlite")


class Employee(Model):
    first_name = TextField(null=False, verbose_name="First Name")
    last_name = TextField(null=False, verbose_name="Last Name")
    birthday = DateField(formats=['%Y%m%d'], null=False, verbose_name="Birthday")
    national_code = TextField(unique=True, null=False, verbose_name="National Code")

    class Meta:
        database = db
        db_table = "Employee"

    @classmethod
    def get_all_field_names(cls):
        return [field.verbose_name for field in cls._meta.sorted_fields if field.verbose_name is not None]

    @staticmethod
    def get_all():
        '''
        :return:ModelSelect
        '''
        rows = Employee.select()
        # for row in rows:
        #     print("first_name: {} last_name: {} birthday: {} national_code:{}".format(row.first_name, row.last_name,
        #                                                                               row.birthday,
        #                                                                               row.national_code))
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
    def get_by_national_code(national_code):
        employee = Employee.select().where(Employee.national_code == national_code).first()
        return employee

    @staticmethod
    def search_name(first_name):
        employee = Employee.select().where(Employee.first_name.startswith(first_name))
        return employee

    @staticmethod
    def delete_by_national_code(national_code):
        if Employee.get_by_national_code(national_code=national_code):
            q = Employee.delete().where(Employee.national_code == national_code)
            q.execute()
            return True

    def update_by_info(self, first_name=None, last_name=None, national_code=None, birthday=None):
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if national_code is not None:
            self.national_code = national_code
        if birthday is not None:
            self.birthday = birthday
        self.save()


Employee.create_table()
