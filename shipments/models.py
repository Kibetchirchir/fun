from django.db import models
from users.validators import validate_phone_number
ShipmentStatus = [
    ("pending", "Pending"),
    ("in_transit", "In Transit"),
    ("delivered", "Delivered")
]

ShipmentType = [
    ("international", "International"),
    ("domestic", "Domestic"),
]

class Shipment(models.Model):
    shipment_date = models.DateField(auto_now_add=True)
    shipment_status = models.CharField(max_length=255, choices=ShipmentStatus, default="pending")
    shipment_type = models.CharField(max_length=255, choices=ShipmentType)
    shipment_weight = models.FloatField()
    shipment_volume = models.FloatField()
    shipment_value = models.FloatField()
    country_of_origin = models.CharField(max_length=255)
    location_of_origin = models.CharField(max_length=255)
    country_of_destination = models.CharField(max_length=255)
    location_of_destination = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, validators=[validate_phone_number])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tin = models.CharField(max_length=255, null=True, blank=True)
    passport_number = models.CharField(max_length=255, null=True, blank=True)
