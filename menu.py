from prettytable import PrettyTable
from os import system, name
from model import Employee
from collections import namedtuple
from validation import *


def clear():
    system('clear')


class MainMenu:
    employee_fields_name = ["First Name", "LastName", "Birthday", "National Code"]

    def __init__(self):
        self.menu = {
            1: self.show_employee,
            2: self.search_employee,
            3: self.add_employee,
            4: self.remind_birthday}

    @staticmethod
    def show_menu():
        print("Menu:")
        print("1. show")
        print("2. search")
        print("3. add")
        print("4. birthday")

    def show_employee(self):
        result = Employee.get_all()
        my_table = PrettyTable(self.employee_fields_name)
        for row in result:
            my_table.add_row([row.first_name, row.last_name, row.birthday, row.national_code])
        print(my_table)
        input("Press any key to continue...")

    def search_employee(self):
        pass

    @staticmethod
    def add_employee():
        add_employee = AddEmployeeMenu()
        add_employee.show()
        input("Press any key to continue...")

    def remind_birthday(self):
        pass

    def show(self):
        while True:
            clear()
            self.show_menu()
            choice = int(input("Enter your choice (1-5): "))
            if choice == len(self.menu) + 1:
                print("bye")
                break
            func = self.menu.get(choice)
            if func:
                func()
            else:
                print("Invalid choice.")


class AddEmployeeMenu:
    Model = namedtuple('Model', ['first_name', 'last_name', 'birthday', 'national_code', 'is_valid'])

    def __init__(self):
        self.menu = {
            1: self.submit
        }
        self.model = self.Model('', '', '', '', False)

    def get_employee_data(self):
        print("Please Enter Employee Information:")
        first_name = self.get_employee_field(self.model.first_name, 'first name')
        last_name = self.get_employee_field(self.model.last_name, 'last name')
        birthday = self.get_employee_field(self.model.birthday, 'birthday')
        national_code = self.get_employee_field(self.model.national_code, 'national_code')
        self.model = self.Model(first_name, last_name, birthday, national_code, False)

    @staticmethod
    def get_employee_field(model_field, model_field_name):
        field = str(input(f"{model_field_name} ({model_field}): " if model_field else f"{model_field_name}: "))
        if not field:
            field = model_field
        return field

    def submit(self):
        if not self.model.is_valid:
            print('Cannot add to database, please re-enter information')
            return
        result = Employee.add(first_name=self.model.first_name,
                              last_name=self.model.last_name,
                              birthday=self.model.birthday,
                              national_code=self.model.national_code)
        # TODO validate result later
        print("Successfully added.")
        return True

    @staticmethod
    def show_menu():
        print("1 - Submit")
        print("2 - Re-enter Information")
        print("3 - Cancel")

    def validate(self):
        errors = {}
        valid, error = NameValidator.validate(self.model.first_name)
        if not valid:
            errors['first_name'] = error
        valid, error = NameValidator.validate(self.model.last_name)
        if not valid:
            errors['last_name'] = error

        valid, error = BirthdayValidator.validate(self.model.birthday)
        if not valid:
            errors['birthday'] = error

        valid, error = NationalCodeValidator.validate(self.model.national_code)
        if not valid:
            errors['national_code'] = error

        for field, error in errors.items():
            print(f'Validation Error, {field}: {error}')
        self.model = self.model._replace(is_valid=not bool(errors))

    def show(self):
        while True:
            self.get_employee_data()
            self.validate()
            self.show_menu()
            choice = int(input("enter your choice [1-3]: "))
            func = self.menu.get(choice)
            if choice == len(self.menu) + 2:
                return
            if func:
                if func():
                    return


class Search:

    def __int__(self):
        self.menu = {
            1: self.similar_search,
            2: self.exactly_search

        }

    def similar_search(self, first_name):
        pass

    def exactly_search(self, national_code):
        pass

    @staticmethod
    def show_menu():
        print("1-similar_search: ")
        print("2-exactly_search: ")
