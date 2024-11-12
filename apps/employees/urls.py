from .import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register("", views.EmployeViewSet, basename="employees")

urlpatterns = [
    path('', include(router.urls)),
]