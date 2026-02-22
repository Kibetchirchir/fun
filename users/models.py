from django.db import models
from .validators import validate_nid, validate_phone_number
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from utils.notification import queue_notification

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
    def get_by_natural_key(self, email):
        """Needed by Django authenticate()"""
        return self.get(email=email)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, validators=[validate_phone_number])
    password = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=[("admin", "Admin"), ("agent", "Agent"), ("customer", "Customer")])
    nid = models.CharField(max_length=16, validators=[validate_nid])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_sector = models.CharField(max_length=20, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    last_otp_sent = models.DateTimeField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = "email"       
    REQUIRED_FIELDS = ["type"] 

    def __str__(self):
        return self.email

