from rest_framework import serializers
from shipments.models import Shipment
from users.validators import validate_phone_number
from shipments.models import ShipmentStatus
class ShipmentSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Shipment
        fields = '__all__'
    
    def validate_phone_number(self, phone_number):
        if not validate_phone_number(phone_number):
            raise serializers.ValidationError("Phone number must be 12 digits and must start with 250")
        return phone_number


class ShipmentUpdateStatusSerializer(serializers.ModelSerializer):
    shipment_status = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Shipment
        fields = ['shipment_status']
    
    def validate_shipment_status(self, shipment_status):

        if shipment_status not in ["pending", "in_transit", "delivered"]:
            raise serializers.ValidationError("Invalid shipment status")
        return shipment_status


class ShipmentUpdateBulkStatusSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), required=True)
    status = serializers.CharField(max_length=255, required=True)
    class Meta:
        fields = ['ids', 'status']
    
    def validate_ids(self, ids):
        if not ids:
            raise serializers.ValidationError("ids are required")
        return ids
    
    def validate_status(self, status):
        if status not in ["pending", "in_transit", "delivered"]:
            raise serializers.ValidationError("Invalid shipment status")
        return status