from .import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('', views.OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
]
