import phonenumbers
from validate_email import validate_email
import re


def password_validator(password):
    flag = 0
    while True:
        if (len(password) <= 8):
            flag = -1
            break
        elif not re.search("[a-z]", password):
            flag = -1
            break
        elif not re.search("[A-Z]", password):
            flag = -1
            break
        elif not re.search("[0-9]", password):
            flag = -1
            break
        elif not re.search("[_@$]", password):
            flag = -1
            break
        elif re.search("\s", password):
            flag = -1
            break
        else:
            flag = 0
            print("Valid Password")
            break

    if flag == -1:
        print("Not a Valid Password ")


def email_validator(email):
    return validate_email(email)


def phone_validator(phone):
    return phonenumbers.is_possible_number(phonenumbers.parse(phone))
