import datetime
import os
import view

# os.system('clear')
while True:
    print(" 1- show all employees\n 2- search for employees\n 3- add new employees")
    choice = int(input("please enter your choice: "))
    if choice in [1, 2, 3]:
        if choice == 1:
            view.show_employee()
        elif choice == 2:
            print("1-first_name:\n2-last_name:\n3-birthday\n4-national_code")
            select_case = int(input("plz enter one of top options:"))
            first_name = None
            last_name = None
            birthday = None
            national_code = None
            if select_case == 1:
                first_name = str(input("plz enter first_name: "))
            elif select_case == 2:
                last_name = str(input("plz enter last_name: "))
            elif select_case == 3:
                birthday = str(input("plz enter birthday: "))
            elif select_case == 4:
                national_code = str(input("plz enter national_code: "))
            view.search_employee(first_name=first_name,last_name=last_name, birthday= birthday, national_code=national_code)
        elif choice == 3:
            view.add_employee()

    else:
        continue
