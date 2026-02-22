from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from shipments.models import Shipment
from shipments.serializers import ShipmentUpdateStatusSerializer, ShipmentUpdateBulkStatusSerializer, ShipmentSerializer
from shipments.utils import update_bulk_shipment_status_queue
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
    def list(self, request):
        shipments = self.queryset.all()
        serializer = self.serializer_class(shipments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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