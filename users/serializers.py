from rest_framework import serializers
from .models import User
from .validators import validate_nid
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
import random


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    nid = serializers.CharField(required=False, write_only=True)
    yob = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'type', "email", "assigned_sector", "password", "nid", "yob"]
        extra_kwargs = {
            "password": {"write_only": True}
        }



      
    
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return password
    
    def validate_nid(self, nid):
        validate_nid(nid, self.initial_data.get('yob'))
        return nid

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)


class NIDSerializer(serializers.Serializer):
    nid = serializers.CharField(required=True)

class AgentOnboardSerializer(UserSerializer):
    nid = serializers.CharField(required=True)
    password = serializers.CharField(required=False, write_only=True)
    
    def create(self, validated_data):
        validated_data["type"] = "agent"
        return User.objects.create(**validated_data)
        
class LoginSessionSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return attrs
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        new_password = attrs.get('new_password')
        return attrs

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        return attrs

class InitiatePasswordRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        return attrs