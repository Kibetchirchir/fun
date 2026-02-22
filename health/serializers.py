from rest_framework import serializers

class HealthSerializer(serializers.Serializer):
    class Meta:
        fields = ['status']