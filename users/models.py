from django.db import models
from .validators import validate_nid, validate_phone_number
# Create your models here.


class User(models.Model):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number])
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=[("admin", "Admin"), ("agent", "Agent"), ("customer", "Customer")])
    nid = models.CharField(max_length=16, validators=[validate_nid])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email