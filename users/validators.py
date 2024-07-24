import re
from django.core.exceptions import ValidationError

def validate_phone_number(phone_number):
    if not re.match(r'09[0-9]{8}', phone_number):
        raise ValidationError('Phone number not the valid format.')
        