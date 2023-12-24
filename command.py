import click
from common import print_employees
from model import Employee
from callback import name_validator, birthday_validator, national_code_validator


@click.group()
def operations():
    pass


def abort_if_false(ctx, param, value):
    if not value:
        click.echo(f"return")


@operations.command(name="show")
@click.option("-n", "--national_code", callback=national_code_validator,
              help="Will show specific employee.", type=str)
@click.option("-a", "--all", is_flag=True, help="Will show all employees.")
def show(all, national_code):
    if all:
        print_employees(list(Employee.get_all()), Employee.get_all_field_names())
    elif national_code is not None:
        print_employees(Employee.get_by_national_code(national_code), Employee.get_all_field_names())


@operations.command(name="add")
@click.option("--first_name", prompt="First Name", type=str, callback=name_validator,
              help="It is the employee's name")
@click.option("--last_name", prompt="Last Name", type=str, callback=name_validator,
              help="It is the employee's last name")
@click.option("--birthday", prompt="Birthday", type=str, callback=birthday_validator,
              help="It is the employee's birthday")
@click.option("--national_code", prompt="National Code", type=str, callback=national_code_validator, help="It is the employee's national code")
def add(first_name, last_name, birthday, national_code):
    Employee.add(first_name, last_name, birthday, national_code)
    click.echo("Employee added successfully")


@operations.command(name="delete")
@click.option("-n", "--national_code", prompt="National Code", callback=national_code_validator,
              help="It is the employee's national code", type=str)
@click.option('--yes', is_flag=True, expose_value=True, prompt='Are you sure you want to delete from db?')
def delete(national_code, yes):
    if yes:
        Employee.delete_by_national_code(national_code)
        click.echo("Employee deleted successfully")


@operations.command(name="update")
@click.option("-n", "--national_code", prompt="National Code", type=str, help="It is the employee's national code")
@click.option("--new_first_name", type=str, help="It is the employee's name")
@click.option("--new_last_name", type=str, help="It is the employee's last name")
@click.option("--new_birthday", type=str, help="It is the employee's birthday")
@click.option("--new_national_code", type=str, help="It is the employee's national code")
@click.option('--yes', is_flag=True, expose_value=True, prompt='Are you sure you want to update the employee?')
def update(national_code, new_first_name, new_last_name, new_birthday, new_national_code, yes):
    if yes:
        employee = Employee.get_by_national_code(national_code)
        if employee:
            Employee.update_by_info(employee, first_name=new_first_name, last_name=new_last_name,
                                birthday=new_birthday, national_code=new_national_code)
            click.echo("employee updated successfully")
        else:
            click.echo("Employee not found")

#






