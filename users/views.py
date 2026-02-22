from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, NIDSerializer, AgentOnboardSerializer
from rest_framework.views import APIView


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