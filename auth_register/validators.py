import phonenumbers
from validate_email import validate_email
import re


def password_validator(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search(r"[^\w\s]", password):
        return False
    return True


def email_validator(email):
    return validate_email(email)


def phone_validator(phone) -> tuple:
    if phone.startswith(('7', '8')):
        phone = '+7' + phone[1:]
    try:
        parsed_phone = phonenumbers.parse(phone, 'RU')
        return phonenumbers.is_possible_number(parsed_phone), phone
    except phonenumbers.phonenumberutil.NumberParseException:
        return False, ""
