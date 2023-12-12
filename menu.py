import datetime
from datetime import date

import model
from prettytable import PrettyTable
from os import system, name
from model import *
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
            4: self.remind_birthday,
            5: self.delete_employee}

    @staticmethod
    def show_menu():
        print("Menu:")
        print("1. show")
        print("2. search")
        print("3. add")
        print("4. birthday")
        print("5. delete")
        print("6. exit")

    def show_employee(self):
        result = Employee.get_all()
        self.print_employees(result)
        input("Press any key to continue...")

    @staticmethod
    def print_employees(employees):
        if employees:
            my_table = PrettyTable(MainMenu.employee_fields_name)
            for row in employees:
                my_table.add_row([row.first_name, row.last_name, row.birthday, row.national_code])
            print(my_table)
        else:
            print("does not exist")

    @staticmethod
    def search_employee():
        search_employee = SearchEmployeeMenu()
        search_employee.show()

    @staticmethod
    def add_employee():
        add_employee = AddEmployeeMenu()
        add_employee.show()
        input("Press any key to continue...")

    def remind_birthday(self):
        birthday_menu = BirthdayMenu()
        birthday_menu.show()

    @staticmethod
    def delete_employee():
        delete_employee = DeleteEmployeeMenu()
        delete_employee.show()
        # input("Press any key to continue")

    def show(self):
        while True:
            # clear()
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
    ModelSample = namedtuple('Model', ['first_name', 'last_name', 'birthday', 'national_code', 'is_valid'])

    def __init__(self):
        self.menu = {
            1: self.submit
        }
        self.model = self.ModelSample('', '', '', '', False)

    def get_employee_data(self):
        print("Please Enter Employee Information:")
        first_name = self.get_employee_field(self.model.first_name, 'first name')
        last_name = self.get_employee_field(self.model.last_name, 'last name')
        birthday = self.get_employee_field(self.model.birthday, 'birthday(like:2023-01-30)')
        national_code = self.get_employee_field(self.model.national_code, 'national_code')
        self.model = self.ModelSample(first_name, last_name, birthday, national_code, False)

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


class SearchEmployeeMenu:

    def __init__(self):
        self.menu = {
            1: self.search_by_name,
            2: self.search_by_national_code

        }

    def search_by_name(self):
        first_name = str(input("First Name: "))
        valid, error = self.validate_first_name(first_name)
        if valid:
            employees = Employee.search_name(first_name)
            MainMenu.print_employees(employees)
        else:
            print(error)
        input("Press any key to continue...")
        return True

    def search_by_national_code(self):
        national_code = str(input("National Code: "))
        valid, error = self.validate_national_code(national_code)
        if valid:
            employees = Employee.search_national_code(national_code)
            MainMenu.print_employees(employees)
        else:
            print(error)
        input("Press any key to continue...")
        return True

    @staticmethod
    def validate_first_name(firstname):
        valid, error = NameValidator.validate(firstname)
        if valid:
            return True, ""
        else:
            return False, error

    @staticmethod
    def validate_national_code(national_code):
        valid, error = NationalCodeValidator.validate(national_code)
        if valid:
            return True, ""
        else:
            return False, error

    @staticmethod
    def show_menu():
        print("1- Search By Name")
        print("2- Search By National Code")
        print("3- Cancel")

    def show(self):
        while True:
            self.show_menu()
            choice = int(input("enter your choice [1-3]: "))
            func = self.menu.get(choice)
            if choice == len(self.menu) + 1:
                return
            if func:
                if func():
                    return


class DeleteEmployeeMenu:

    def __init__(self):
        self.menu = {1: self.delete}
        self.national_code = ""
        self.is_valid = False

    def delete(self):
        if self.is_valid:
            print("Are you sure ? ")
            choice = str(input("Enter Yes/No : "))
            if choice.lower() in ("yes" or "y"):
                if Employee.delete_by_national_code(self.national_code):
                    print("Successfully deleted.")
                else:
                    print("does not exist.")
        else:
            print('Cannot delete from database, please re-enter national code')

    @staticmethod
    def show_menu():
        print("1- Delete Employee")
        print("2- Re-enter National Code")
        print("3- Cancel")

    def get_national_code(self):
        national_code = str(input("National Code: "))
        self.national_code = national_code

    def validate(self):
        valid, error = NationalCodeValidator.validate(self.national_code)
        if valid:
            self.is_valid = True
        else:
            print(f"error = {error}")

    def show(self):
        while True:
            self.get_national_code()
            self.validate()
            self.show_menu()
            choice = int(input("enter your choice [1-3]: "))
            func = self.menu.get(choice)
            if choice == len(self.menu) + 2:
                return
            if func:
                func()
                return


class BirthdayMenu:
    def __init__(self):
        self.menu = {1: self.calculate_remaining_days}
        self.national_code = ""
        self.is_valid = False

    def calculate_remaining_days(self):
        if self.is_valid:
            birthday = self.get_birthday()
            if not birthday:
                print("The employee not found")
                return
            days_to_birthday = self.get_num_of_days(birthday)
            print(f"There are {days_to_birthday} days to his/her birthday")
            input("Press any key to continue...")
            return True
        else:
            print('Cannot find employee, please re-enter national code')

    def get_national_code(self):
        national_code = str(input("National Code: "))
        self.national_code = national_code

    def validate(self):
        valid, error = NationalCodeValidator.validate(self.national_code)
        if valid:
            self.is_valid = True
        else:
            print(error)

    def get_birthday(self):
        employee = Employee.search_national_code(self.national_code)
        if employee:
            birthday = datetime.datetime.strptime(employee[0].birthday, "%Y-%m-%d")
            return birthday

    @staticmethod
    def get_num_of_days(birthday):
        now = datetime.datetime.now()
        birthday = datetime.datetime(now.year, birthday.month, birthday.day)
        if now > birthday:
            birthday = datetime.datetime(birthday.year + 1, birthday.month, birthday.day)
        return (birthday - now).days

    @staticmethod
    def show_menu():
        print("1- Calculate Birthday Remaining Days")
        print("2- Re-enter National Code")
        print("3- Cancel")

    def show(self):
        while True:
            self.get_national_code()
            self.validate()
            self.show_menu()
            choice = int(input("enter your choice [1-3]: "))
            func = self.menu.get(choice)
            if choice == len(self.menu) + 2:
                return
            if func:
                if func():
                    return
