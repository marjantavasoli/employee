import click
from common import print_employees
from model import Employee
from validation import NationalCodeValidator, NameValidator, BirthdayValidator


@click.group()
def operations():
    pass


def abort_if_false(ctx, param, value):
    if not value:
        click.echo(f"return")


@operations.command(name="show")
@click.option("-a", "--all", is_flag=True, help="Will show all employees.")
@click.option("-n", "--national_code", help="Will show specific employee.", type=str)
def show(all, national_code):
    if all:
        print_employees(Employee.get_all(), Employee.get_all_field_names())
    elif national_code is not None:
        valid, error = NationalCodeValidator.validate(national_code)
        if valid:
            print_employees([Employee.get_by_national_code(national_code)], Employee.get_all_field_names())
        else:
            click.echo(f"{error}")


@operations.command(name="add")
@click.option("--first_name", prompt="First Name", type=str, help="It is the employee's name")
@click.option("--last_name", prompt="Last Name", type=str, help="It is the employee's last name")
@click.option("--birthday", prompt="Birthday", type=str, help="It is the employee's birthday")
@click.option("--national_code", prompt="National Code", type=str, help="It is the employee's national code")
def add(first_name, last_name, birthday, national_code):
    valid = True
    errors = []
    valid_name, error_name = NameValidator.validate(first_name)
    valid = valid_name and valid
    errors.append(error_name)
    valid_name, error_name = NameValidator.validate(last_name)
    valid = valid_name and valid
    errors.append(error_name)
    valid_birthday, error_birthday = BirthdayValidator.validate(birthday)
    valid = valid_birthday and valid
    errors.append(error_birthday)
    valid_national_cod, error_national_code = NationalCodeValidator.validate(national_code)
    valid = valid_national_cod and valid
    errors.append(error_national_code)
    if valid:
        Employee.add(first_name, last_name, birthday, national_code)
    else:
        print(errors)  # TODO remove None errors first
        return


@operations.command(name="delete")
@click.option("-n", "--national_code", prompt="National Code", help="It is the employee's national code", type=str)
@click.option('--yes', is_flag=True, expose_value=True, prompt='Are you sure you want to delete from db?')
def delete(national_code, yes):
    if yes:
        valid, error = NationalCodeValidator.validate(national_code)
        if valid:
            if Employee.delete_by_national_code(national_code):
                Employee.delete_by_national_code(national_code)
                print("Employee deleted")
            else:
                print("Employee does not exist")
        else:
            print(f"{error}")
            return


@operations.command(name="update")
@click.option("-n", "--national_code", prompt="National Code", type=str, help="It is the employee's national code")
@click.option("--new_first_name", type=str, help="It is the employee's name")
@click.option("--new_last_name", type=str, help="It is the employee's last name")
@click.option("--new_birthday", type=str, help="It is the employee's birthday")
@click.option("--new_national_code", type=str, help="It is the employee's national code")
@click.option('--yes', is_flag=True, expose_value=True, prompt='Are you sure you want to update the employee?')
def update(national_code, new_first_name, new_last_name, new_birthday, new_national_code, yes):
    if yes:
        valid, error = NationalCodeValidator.validate(national_code)
        if valid:
            employee = Employee.get_by_national_code(national_code=national_code)
            if employee:
                valid = True
                errors = []
                if new_first_name :
                    valid_name, error_name = NameValidator.validate(new_first_name)
                    valid = valid_name and valid
                    errors.append(error_name)
                if new_last_name:
                    valid_name, error_name = NameValidator.validate(new_last_name)
                    valid = valid_name and valid
                    errors.append(error_name)
                if new_birthday:
                    valid_birthday, error_birthday = BirthdayValidator.validate(new_birthday)
                    valid = valid_birthday and valid
                    errors.append(error_birthday)
                if new_national_code:
                    valid_national_cod, error_national_code = NationalCodeValidator.validate(new_national_code)
                    valid = valid_national_cod and valid
                    errors.append(error_national_code)
                if valid:
                    Employee.update_by_info(employee, first_name=new_first_name, last_name=new_last_name, birthday=new_birthday, national_code=new_national_code)
                    print("employee updated")
                else:
                    print(errors)
                    return

            else:
                print("Employee does not exist")
        else:
            print(f"{error}")








