from django.urls import path
from domestic.views import DomesticShipmentView


urlpatterns = [
    path('', DomesticShipmentView.as_view({'post': 'create'}), name='create-domestic-shipment'),
]