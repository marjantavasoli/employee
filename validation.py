import abc
import datetime
import re
import _strptime
import time


class Validator(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def validate(cls, value) -> (bool, str):
        pass


class NameValidator(Validator):

    @classmethod
    def validate(cls, value) -> (bool, str):
        value = value.replace(" ", "")
        if value == "":
            return False, "it is required"
        match = re.fullmatch("[a-zA-Z ]*", value)
        if match is None:
            return False, 'Please enter only characters or space'
        return True, ""


class BirthdayValidator(Validator):

    @classmethod
    def validate(cls, value) -> (bool, str):
        try:
            value = value.replace("-", "").replace("/", "").replace(" ", "")
            if value == "":
                return False, "it is required"
            value = datetime.datetime.strptime(value, "%Y%m%d")
            return True, ""

        except ValueError:
            return False, "Please enter valid date"


class NationalCodeValidator(Validator):
    @classmethod
    def validate(cls, value) -> (bool, str):
        value = value.strip(" ")
        if value == "":
            return False, "it is required."
        if len(value) == 10 and re.fullmatch("\d{10}",value):
            return True, ""
        return False, "Please enter only number"







# n = NameValidator.validate("jdhfoh")
# print(n)
