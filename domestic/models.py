from shipments.models import Shipment

class DomesticShipment(Shipment):

    class Meta:
        verbose_name = "Domestic Shipment"