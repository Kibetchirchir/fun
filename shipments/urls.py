from django.urls import path
from shipments.views import ShipmentUpdateStatusView


urlpatterns = [
    path('<int:pk>/update_status/', ShipmentUpdateStatusView.as_view({'put': 'update_status'}), name='update-shipment-status'),
]