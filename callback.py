import click
from validation import NameValidator, NationalCodeValidator, BirthdayValidator


def name_validator(ctx, param, value):
    if value is not None:
        valid_name, error = NameValidator.validate(value)
        if not valid_name:
            raise click.ClickException(error)
    return value


def national_code_validator(ctx, param, value):
    if value is not None:
        valid_national_code, error = NationalCodeValidator.validate(value)
        if not valid_national_code:
            raise click.BadParameter(error)
    return value


def birthday_validator(ctx, param, value):
    if value is not None:
        valid_birthday, error = BirthdayValidator.validate(value)
        if not valid_birthday:
            raise click.ClickException(error)

    return value
