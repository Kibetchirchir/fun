from shipments.serializers import ShipmentSerializer
from international.models import InternationalShipment
from rest_framework import serializers

class InternationalShipmentSerializer(ShipmentSerializer):
    tin = serializers.CharField(max_length=255, required=True)
    passport_number = serializers.CharField(max_length=255, required=True)
    shipment_type = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = InternationalShipment
        fields = '__all__'
    
    def validate(self, attrs):
        attrs['shipment_type'] = "international"
        return attrs
