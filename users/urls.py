from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from .views import UserViewSet, SigninView, LoginView, RefreshTokenView, LogoutView, CookieJWTAuthenticatation, MeView, ProtectedView, ProfileView, RegisterView


router = DefaultRouter()
router.register(r'profile', ProfileView, basename='profile')

urlpatterns = [
    path('signin/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_blacklist'),
    path('me/', MeView.as_view(), name='me'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]