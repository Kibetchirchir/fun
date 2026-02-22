import re
from django.core.exceptions import ValidationError


def validate_nid(nid, yob):
    """
    Validates a NID:
    - Must be exactly 16 digits
    """
    pattern = r'^\d{16}$'
    if not re.match(pattern, nid):
        raise ValidationError(
            "NID must be 16 digits"
        )
    yob_id = nid[0:4]

    if str(yob_id) != str(yob):
        raise ValidationError(
            "Year of birth does not match the NID"
        )
    return nid
def validate_phone_number(phone_number):
    """
    Validates a phone number:
    - Must be exactly 12 digits
    - Must start with 250
    """
    pattern = r'^250\d{9}$'
    if not re.match(pattern, phone_number):
        raise ValidationError(
            "Phone number must be 12 digits and must start with 250"
        )
    return phone_number

