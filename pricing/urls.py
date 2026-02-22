from django.urls import path
from pricing.views import PricingView

urlpatterns = [
    path('', PricingView.as_view({'post': 'create'}), name='pricing-create'),
    path('tarrifs/', PricingView.as_view({'get': 'get_tarrifs'}), name='pricing-get-tarrifs'),
    path('calculate/', PricingView.as_view({'post': 'calculate_price'}), name='pricing-calculate-price'),
]