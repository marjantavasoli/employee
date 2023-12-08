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


n = NameValidator.validate("jdhfoh")
print(n)
