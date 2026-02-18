from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, NIDSerializer
from rest_framework.decorators import api_view


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

@api_view(["POST"])
def verify_nid(request):
    serializer = NIDSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({"message": "NID is valid"}, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_user(request):
    user = request.headers.get("email")
    print(user)
    if not user:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(email=user)
    if not user:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)