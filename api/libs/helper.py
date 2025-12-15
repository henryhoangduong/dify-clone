import re
import subprocess
import uuid
from datetime import datetime
from zoneinfo import available_timezones
import random
import string

from flask_restful import fields


def run(script):
    return subprocess.getstatusoutput('source /root/.bashrc && ' + script)


class TimestampField(fields.raw):
    def format(self, value):
        return int(value.timestamp())


def email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email) is not None:
        return email

    error = ('{email} is not a valid email.'
             .format(email=email))
    raise ValueError(error)


def uuid_value(value):
    if value == '':
        return str(value)

    try:
        uuid_obj = uuid.UUID(value)
        return str(uuid_obj)
    except ValueError:
        error = ('{value} is not a valid uuid.'
                 .format(value=value))
        raise ValueError(error)


def generate_string(n):
    letters_digits = string.ascii_letters + string.digits
    result = ""
    for i in range(n):
        result += random.choice(letters_digits)

    return result
