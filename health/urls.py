from django.urls import path

from health import views

urlpatterns = [
    path("", views.HealthView.as_view(), name="health"),
]
