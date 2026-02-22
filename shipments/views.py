from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from shipments.models import Shipment
from shipments.serializers import ShipmentUpdateStatusSerializer

class ShipmentUpdateStatusView(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Shipment.objects.all()
    serializer_class = ShipmentUpdateStatusSerializer
    def update_status(self, request, pk):
        shipment = self.queryset.get(id=pk)
        serializer = self.serializer_class(
            shipment, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)