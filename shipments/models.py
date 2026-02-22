from django.db import models
from users.validators import validate_phone_number
from utils.notification import queue_notification

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


    def save(self, *args, **kwargs):
        if self.pk:
            previous = Shipment.objects.get(pk=self.pk)
            if previous.shipment_status != self.shipment_status:
                message = f"Your shipment status changed to {self.shipment_status}"
                queue_notification(self.phone_number, message, queue_name="priority")

        super().save(*args, **kwargs)
