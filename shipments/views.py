from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from shipments.models import Shipment
from shipments.serializers import ShipmentUpdateStatusSerializer, ShipmentUpdateBulkStatusSerializer, ShipmentSerializer
from shipments.utils import update_bulk_shipment_status_queue
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

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


class ShipmentUpdateBulkStatusView(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Shipment.objects.all()
    serializer_class = ShipmentUpdateBulkStatusSerializer

    def update_bulk_status(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_id = update_bulk_shipment_status_queue(serializer.validated_data['ids'], serializer.validated_data['status'])
        return Response({"message": f"Processing started for {len(serializer.validated_data['ids'])} shipments", "task_id": job_id, "status": "queued"}, status=status.HTTP_200_OK)

class ShipmentView(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['shipment_status', 'created_at', 'updated_at', 'shipment_type', 'country_of_origin', 'country_of_destination', 'location_of_origin', 'location_of_destination']
    search_fields = ['phone_number', 'tin', 'passport_number']
    
    def retrieve(self, request, pk=None):
        try:
            shipment = self.queryset.get(pk=pk)
        except Shipment.DoesNotExist:
            return Response(
                {"detail": "Shipment not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(shipment)
        return Response(serializer.data, status=status.HTTP_200_OK)