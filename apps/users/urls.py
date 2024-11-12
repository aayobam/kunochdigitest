from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter(trailing_slash=False)
router.register("", views.UserViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
    path("auth", views.CustomTokenObtainPairView.as_view(), name="access_token"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
