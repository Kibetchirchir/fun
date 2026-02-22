from rest_framework import serializers
from pricing.models import Pricing

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'

class CalculatePriceSerializer(serializers.Serializer):
    weight = serializers.FloatField()
    zone = serializers.CharField(max_length=255)
    class Meta:
        fields = ['weight', 'zone']
    
    def validate_weight(self, weight):
        if weight <= 0:
            raise serializers.ValidationError("Weight must be greater than 0")
        return weight