from django.urls import path
from international.views import InternationalShipmentView


urlpatterns = [
    path('', InternationalShipmentView.as_view({'post': 'create'}), name='create-international-shipment'),
    ]