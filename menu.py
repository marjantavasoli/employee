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
            5: self.delete_employee,
            6: self.update_employee}

    @staticmethod
    def show_menu():
        print("Menu:\n1. show\n2. search\n3. add\n4. birthday\n5. delete\n6. update\n7. exit")

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
            print('*' * 30)
        else:
            print("does not exist")
            print('*' * 30)

    @staticmethod
    def search_employee():
        search_employee = SearchEmployeeMenu()
        search_employee.show()

    @staticmethod
    def add_employee():
        add_employee = AddEmployeeMenu()
        add_employee.show()
        input("Press any key to continue...")

    @staticmethod
    def remind_birthday():
        birthday_menu = BirthdayMenu()
        birthday_menu.show()

    @staticmethod
    def delete_employee():
        delete_employee = DeleteEmployeeMenu()
        delete_employee.show()
        # input("Press any key to continue")

    @staticmethod
    def update_employee():
        update_employee = UpdateEmployeeMenu()
        update_employee.show()

    def show(self):
        try:
            while True:
                # clear()
                self.show_menu()
                choice = int(input("Enter your choice (1-5): "))
                print('*' * 30)
                if choice == len(self.menu) + 1:
                    print("bye")
                    break
                func = self.menu.get(choice)
                if func:
                    func()
                else:
                    print("Invalid choice.")
                    print('*' * 30)
        except ValueError:
            print("Please enter only number")
            print('*' * 30)


class AddEmployeeMenu:
    ModelSample = namedtuple('Model', ['first_name', 'last_name', 'birthday', 'national_code', 'is_valid'])

    def __init__(self):
        self.menu = {
            1: self.submit
        }
        self.model_sample = self.ModelSample('', '', '', '', False)

    def get_employee_data(self):
        print("Please Enter Employee Information:")
        first_name = self.get_employee_field(self.model_sample.first_name, 'first name')
        last_name = self.get_employee_field(self.model_sample.last_name, 'last name')
        birthday = self.get_employee_field(self.model_sample.birthday, 'birthday(like:2023-01-30)')
        national_code = self.get_employee_field(self.model_sample.national_code, 'national_code')
        self.model_sample = self.ModelSample(first_name, last_name, birthday, national_code, False)

    @staticmethod
    def get_employee_field(model_field, model_field_name):
        field = str(input(f"{model_field_name} ({model_field}): " if model_field else f"{model_field_name}: "))
        if not field:
            field = model_field
        return field

    def submit(self):
        if not self.model_sample.is_valid:
            print('Cannot add to database, please re-enter information')
            return
        result = Employee.add(first_name=self.model_sample.first_name,
                              last_name=self.model_sample.last_name,
                              birthday=self.model_sample.birthday,
                              national_code=self.model_sample.national_code)
        # TODO validate result later
        print("Successfully added.")
        return True

    @staticmethod
    def show_menu():
        print("1 - Submit\n2 - Re-enter Information\n3 - Cancel")

    def validate(self):
        errors = {}
        valid, error = NameValidator.validate(self.model_sample.first_name)
        if not valid:
            errors['first_name'] = error
        valid, error = NameValidator.validate(self.model_sample.last_name)
        if not valid:
            errors['last_name'] = error

        valid, error = BirthdayValidator.validate(self.model_sample.birthday)
        if not valid:
            errors['birthday'] = error

        valid, error = NationalCodeValidator.validate(self.model_sample.national_code)
        if not valid:
            errors['national_code'] = error

        for field, error in errors.items():
            print(f'Validation Error, {field}: {error}')
        self.model_sample = self.model_sample._replace(is_valid=not bool(errors))

    def show(self):
        try:
            while True:
                self.get_employee_data()
                self.validate()
                self.show_menu()
                choice = int(input("enter your choice [1-3]: "))
                print('*' * 30)
                func = self.menu.get(choice)
                if choice == len(self.menu) + 2:
                    return
                if func:
                    if func():
                        return
        except ValueError:
            print("Please enter only number")
            print('*' * 30)


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
            MainMenu.print_employees([employees])
        else:
            print(f"error: {error}")
            print('*' * 30)
        input("Press any key to continue...")
        print('*' * 30)
        return True

    def search_by_national_code(self):
        national_code = str(input("National Code: "))
        valid, error = self.validate_national_code(national_code)
        if valid:
            employees = Employee.get_by_national_code1(national_code)
            MainMenu.print_employees(employees)
        else:
            print(f"error: {error}")
            print('*' * 30)
        input("Press any key to continue...")  #TODO a static method pause execution
        print('*' * 30)
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
        print("1- Search By Name\n2- Search By National Code\n3- Cancel")
        print('*' * 30)

    def show(self):
        try:
            while True:
                self.show_menu()
                choice = int(input("enter your choice [1-3]: "))
                print('*' * 30)
                func = self.menu.get(choice)
                if choice == len(self.menu) + 1:
                    return
                if func:
                    if func():
                        return
        except ValueError:
            print("please enter only number")
            print('*' * 30)


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
                    print('*' * 30)
                else:
                    print("does not exist.")
                    print('*' * 30)
        else:
            print('Cannot delete from database, please re-enter national code')
            print('*' * 30)

    @staticmethod
    def show_menu():
        print("1- Delete Employee\n2- Re-enter National Code\n3- Cancel")
        print('*' * 30)

    def get_national_code(self):
        national_code = str(input("National Code: "))
        self.national_code = national_code

    def validate(self):
        valid, error = NationalCodeValidator.validate(self.national_code)
        if valid:
            self.is_valid = True
        else:
            print(f"error = {error}")
            print('*' * 30)

    def show(self):
        try:
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
        except ValueError:
            print("Please enter only number")
            print('*' * 30)


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
                print('*' * 30)
                return
            days_to_birthday = self.get_num_of_days(birthday)
            print(f"There are {days_to_birthday} days to his/her birthday")
            print('*' * 30)
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
            print(f"error: {error}")

    def get_birthday(self):
        employee = Employee.get_by_national_code1(self.national_code)
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
        print("1- Calculate Birthday Remaining Days\n2- Re-enter National Code\n3- Cancel")

    def show(self):
        try:
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
        except ValueError:
            print("please enter only number")
            print('*'*30)


class UpdateEmployeeMenu(AddEmployeeMenu):

    def __init__(self):
        self.menu = {1: self.submit}
        # self.national_code = ""
        self.is_valid = False
        # self.valid_national_code = False

    @staticmethod
    def get_national_code():
        national_code = str(input("National Code: "))
        return national_code

    def set_model_sample(self, employee):
        employee = employee
        self.model_sample = self.ModelSample(first_name=employee.first_name,
                                             last_name=employee.last_name,
                                             national_code=employee.national_code,
                                             birthday=employee.birthday,
                                             is_valid=True)

    def validate_national_code(self, national_code):
        valid, error = NationalCodeValidator.validate(national_code)
        if not valid:
            print(f"error = {error}")
            print('*' * 30)
        return valid

    # def get_employee(self, national_code):
    #     employee = Employee.get_by_national_code(national_code)
    #     if employee:
    #         return employee

    # def submit(self, employee):
    #     if not self.model_sample.is_valid:
    #         print('Cannot add to database, please re-enter information')
    #         return
    #     else:
    #         employee.update_by_info(first_name=self.model_sample.first_name,
    #                                 last_name=self.model_sample.last_name,
    #                                 national_code=self.model_sample.national_code,
    #                                 birthday=self.model_sample.birthday)
    #         print('Successfully updated')
    #         input("Press any key to continue...")
    #         return True
    @staticmethod
    def show_menu():
        print("1 - Update\n2 - Re-enter Information\n3 - Cancel")

    def show(self):
        try:
            while True:
                national_code = self.get_national_code()
                is_valid_national_code = self.validate_national_code(national_code)
                if is_valid_national_code:
                    employee = Employee.get_by_national_code(national_code)
                    if employee :
                        self.set_model_sample(employee)
                        self.get_employee_data()
                        self.validate()
                        self.show_menu()
                        choice = int(input("enter your choice [1-3]: "))
                        print('*' * 30)
                        func = self.menu.get(choice)
                        if choice == len(self.menu) + 2:
                            return
                        if choice == 1:
                            if func(employee):
                                return
                    else:
                        print('This employee does not exist')
                        input("Press any key to continue...")
                        return
                else:
                    input("Press any key to continue...")
                    return

        except ValueError:
            print("Please enter only valid number")
            return







