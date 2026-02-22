from rest_framework import serializers
from shipments.models import Shipment
from users.validators import validate_phone_number
class ShipmentSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Shipment
        fields = '__all__'
    
    def validate_phone_number(self, phone_number):
        if not validate_phone_number(phone_number):
            raise serializers.ValidationError("Phone number must be 12 digits and must start with 250")
        return phone_number
