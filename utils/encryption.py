from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings

print(">>>>>>>>>>", settings.INFERNET_KEY)

fernet = Fernet(settings.INFERNET_KEY.encode())

print(">>>>>>>>>>", settings.INFERNET_KEY.encode())
class EncryptedCharField(models.CharField):

    def get_prep_value(self, value):
        if value is None:
            return value
        encrypted = fernet.encrypt(value.encode())
        return encrypted.decode()

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            decrypted = fernet.decrypt(value.encode())
            return decrypted.decode()
        except Exception as e:
            return value

    def to_python(self, value):
        if value is None:
            return value
        try:
            decrypted = fernet.decrypt(value.encode())
            return decrypted.decode()
        except Exception:
            return value