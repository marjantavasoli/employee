from prettytable import PrettyTable


def print_employees(employees, columns):
    if employees:
        my_table = PrettyTable(columns)
        for row in employees:
            my_table.add_row([row.first_name, row.last_name, row.birthday, row.national_code])
        print(my_table)
    else:
        print("does not exist")
