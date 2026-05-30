from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.api.rest_view import (
    RegisterView, CustomTokenObtainPairView, LogoutView, UserExtendedViewSet, GlobalSearchViewSet,
)

router = DefaultRouter()
router.register(r'users', UserExtendedViewSet, basename='users')
router.register(r'search', GlobalSearchViewSet, basename='search')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
