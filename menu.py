from model import Employee


class MainMenu:
    def __init__(self):
        self.menu = {
            1: self.show_employee,
            2: self.search_employee,
            3: self.add_employee,
            4: self.reminder_birthday}

    @staticmethod
    def show_menu():
        print("Menu:")
        print("1. show")
        print("2. search")
        print("3. add")
        print("4. birthday")

    def show_employee(self):
        Employee.get_all()
        return



    def search_employee(self):
        pass

    @staticmethod
    def add_employee():
        first_name = str(input("plz enter first_name:"))
        last_name = str(input("plz enter last_name:"))
        birthday = str(input("plz enter your birthday:"))
        national_code = str(input("plz enter national_code: "))
        Employee.add(first_name=first_name, last_name=last_name, birthday= birthday, national_code= national_code)

    def reminder_birthday(self):
        pass


    def start(self):
        while True:
            self.show_menu()
            choice = int(input("Enter your choice (1-5): "))
            if choice == len(self.menu)+1:
                print("bye")
                break
            func = self.menu.get(choice)
            if func:
                func()
            else:
                print("Invalid choice.")


