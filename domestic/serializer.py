from shipments.serializers import ShipmentSerializer
from domestic.models import DomesticShipment
from rest_framework import serializers

class DomesticShipmentSerializer(ShipmentSerializer):

    shipment_weight = serializers.FloatField()
    shipment_volume = serializers.FloatField()
    shipment_value = serializers.FloatField()
    country_of_origin = serializers.CharField(max_length=255)
    location_of_origin = serializers.CharField(max_length=255) 
    location_of_destination = serializers.CharField(max_length=255)
    country_of_destination = serializers.CharField(max_length=255, required=False)
    location_of_destination = serializers.CharField(max_length=255, required=False)
    shipment_type = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = DomesticShipment
        fields = '__all__'
    
    def validate(self, attrs):
        attrs['shipment_type'] = "domestic"
        attrs['country_of_destination'] = attrs['country_of_origin']
        return attrs