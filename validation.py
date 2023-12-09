import abc
import re


class Validator(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def validate(cls, value) -> (bool, str):
        pass


class NameValidator(Validator):

    @classmethod
    def validate(cls, value) -> (bool, str):
        value = value.strip(" ")
        if value == "":
            return False, "it is required"
        match = re.fullmatch("[a-zA-Z ]*", value)
        if match is None:
            return False, 'Please enter only characters or space'
        return True, ""


class BirthdayValidator(Validator):

    @classmethod
    def validate(cls, value) -> (bool, str):
        value = value.strip(" ")
        if value == "":
            return False, "it is required"
        if len(value) == 8 and re.fullmatch("^\d{4}\d{2}\d{2}$", value):
            if value[:4:] < '2023' and value[5:6] < str(12) and value[7::] < str(31):
                return True, ""
            else:
                return False, "Please enter valid date"

        return False, "Please enter only number"


class NationalCodeValidator(Validator):
    @classmethod
    def validate(cls, value) -> (bool, str):
        value = value.strip(" ")
        if value == "":
            return False, "it is required."
        if len(value) == 10 and re.fullmatch("\d{10}"):
            return True, ""
        return False, "Please enter only number"







# n = NameValidator.validate("jdhfoh")
# print(n)
