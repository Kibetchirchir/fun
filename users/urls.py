from django.urls import path
from .views import UserViewSet, VerifyNIDView, GetUserView, AgentOnboardView, LoginSessionView, LogoutSessionView, WhoAmIView, PasswordChangeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register/', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('auth/verify-nid/', VerifyNIDView.as_view(), name='verify-nid'),
    path('auth/me/', GetUserView.as_view(), name='get-user'),
    path('auth/agents/onboard/', AgentOnboardView.as_view({'post': 'create'}), name='agent-onboard'),
    path('auth/login/session/', LoginSessionView.as_view(), name='login-session'),
    path('auth/logout/', LogoutSessionView.as_view(), name='logout-session'),
    path('auth/token/obtain/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/whoami/', WhoAmIView.as_view(), name='whoami'),
    path('auth/password/change/', PasswordChangeView.as_view(), name='password-change'),
]
