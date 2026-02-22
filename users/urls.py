from django.urls import path
from .views import UserViewSet, VerifyNIDView, GetUserView, AgentOnboardView, LoginSessionView, LogoutSessionView

urlpatterns = [
    path('auth/register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('auth/verify-nid/', VerifyNIDView.as_view(), name='verify-nid'),
    path('auth/me/', GetUserView.as_view(), name='get-user'),
    path('auth/agents/onboard/', AgentOnboardView.as_view({'post': 'create'}), name='agent-onboard'),
    path('auth/login/session/', LoginSessionView.as_view(), name='login-session'),
    path('auth/logout/', LogoutSessionView.as_view(), name='logout-session'),
]
