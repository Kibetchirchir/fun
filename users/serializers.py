from rest_framework import serializers
from .models import User
from .validators import validate_nid
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'type', "email", "assigned_sector", "password"]


      
    
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return password

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)


class NIDSerializer(serializers.Serializer):
    nid = serializers.CharField(required=True)

    def validate_nid(self, nid):
        try:
            validate_nid(nid)
        except ValidationError as e:
            raise serializers.ValidationError({
                "valid": False,
                "message": str(e.message)
            })

        return nid