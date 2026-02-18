def validate_nid(nid):
    if len(nid) != 16:
        raise ValueError("NID must be 16 digits")
    return nid

def validate_phone_number(phone_number):
    if len(phone_number) != 12:
        raise ValueError("Phone number must be 12 digits")
    if phone_number.startswith("250"):
        raise ValueError("Phone number must not start with 250")
    return phone_number
