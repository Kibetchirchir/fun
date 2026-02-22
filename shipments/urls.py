from django.urls import path
from shipments.views import ShipmentUpdateStatusView, ShipmentUpdateBulkStatusView, ShipmentView


urlpatterns = [
    path('', ShipmentView.as_view({'get': 'list'}), name='shipment-list'),
    path('<int:pk>/', ShipmentView.as_view({'get': 'retrieve'}), name='shipment-detail'),
    path('<int:pk>/update_status/', ShipmentUpdateStatusView.as_view({'put': 'update_status'}), name='update-shipment-status'),
    path('batch-update/', ShipmentUpdateBulkStatusView.as_view({'post': 'update_bulk_status'}), name='update-bulk-shipment-status'),
]