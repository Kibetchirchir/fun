from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from domestic.models import DomesticShipment
from rest_framework.permissions import IsAuthenticated
from domestic.serializer import DomesticShipmentSerializer


# Create your views here.
class DomesticShipmentView(viewsets.ModelViewSet):
    permission_classes = []
    queryset = DomesticShipment.objects.all()
    serializer_class = DomesticShipmentSerializer
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)