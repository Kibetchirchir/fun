from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer, NIDSerializer, AgentOnboardSerializer, LoginSessionSerializer, ResetPasswordSerializer, VerifyOTPSerializer, InitiatePasswordRecoverySerializer, VerifyPasswordRecoverySerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.throttling import ScopedRateThrottle
from utils.redis import cache_set, cache_get, cache_delete
import random
from .validators import validate_nid
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        otp = random.randint(100000, 999999)
        cache_set(f"otp_{serializer.data['email']}", otp, ex=60*5)
        print(f"OTP: {otp}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class AgentOnboardView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AgentOnboardSerializer
    permission_classes = []

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyNIDView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = NIDSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        print(f"User: {user.yob}")
        print(f"NID: {serializer.validated_data["nid"]}")
        try:
            validate_nid(serializer.validated_data["nid"], user.yob)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "NID is valid"}, status=status.HTTP_200_OK)

class GetUserView(APIView):
    permission_classes = []
    queryset = None
    serializer_class = UserSerializer
    def get(self, request):
        user = request.headers.get("email")
        if not user:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=user)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginSessionView(APIView):
    permission_classes = [AllowAny]
    queryset = None
    serializer_class = LoginSessionSerializer
    throttle_scope = "login"
    throttle_classes = [ScopedRateThrottle]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)  

        return Response({
            "id": user.id,
            "email": user.email,
            "type": user.type,
        }, status=status.HTTP_200_OK)

class LogoutSessionView(APIView):
    permission_classes = [IsAuthenticated]
   
    def get(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)

class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = UserSerializer
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = None
    serializer_class = ResetPasswordSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        new_password = serializer.validated_data["new_password"]

        user = request.user
        if not user.check_password(password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    permission_classes = []
    queryset = None
    serializer_class = VerifyOTPSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        cached_otp = cache_get(f"otp_{email}")
        print(f"Cached OTP: {cached_otp} and OTP: {otp}")
        if not cached_otp:
            return Response({"detail": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        if str(cached_otp) != str(otp):
            return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        cache_delete(f"otp_{email}")
        return Response({"detail": "OTP verified successfully"}, status=status.HTTP_200_OK)

class InitiatePasswordRecoveryView(APIView):
    permission_classes = []
    queryset = None
    serializer_class = InitiatePasswordRecoverySerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        otp = random.randint(100000, 999999)
        cache_set(f"otp_{email}", otp, ex=60*5)
        print(f"OTP: {otp}")
        return Response({"detail": "Password recovery initiated successfully"}, status=status.HTTP_200_OK)

class VerifyPasswordRecoveryView(APIView):
    permission_classes = []
    queryset = None
    serializer_class = VerifyPasswordRecoverySerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]
        cached_otp = cache_get(f"otp_{email}")
        if not cached_otp:
            return Response({"detail": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        if str(cached_otp) != str(otp):
            return Response({"detail": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        cache_delete(f"otp_{email}")
        return Response({"detail": "Password recovery verified successfully"}, status=status.HTTP_200_OK)