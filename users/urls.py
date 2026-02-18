from django.urls import path
from .views import UserViewSet, verify_nid

urlpatterns = [
    path('auth/register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('auth/verify-nid/', verify_nid, name='verify-nid'),
]