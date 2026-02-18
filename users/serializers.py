from rest_framework import serializers
from .models import User
from .validators import validate_nid
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'password', 'type', 'nid', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class NIDSerializer(serializers.Serializer):
    nid = serializers.CharField(required=True)

    def validate_nid(self, nid):
        try:
            validate_nid(nid)
        except ValidationError as e:
            raise serializers.ValidationError({
                "valid": False,
                "message": str(e)
            })

        return nid