from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer, NIDSerializer, AgentOnboardSerializer, LoginSessionSerializer, ResetPasswordSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.throttling import ScopedRateThrottle

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
    permission_classes = []
    queryset = None
    serializer_class = NIDSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
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
