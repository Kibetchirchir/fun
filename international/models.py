from django.db import models
from shipments.models import Shipment


class InternationalShipment(Shipment):
    class Meta:
        verbose_name = "International Shipment"