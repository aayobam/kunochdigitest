from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from django.db import transaction
from apps.employees.models import Employee
from apps.employees.serializers import (
    CreateEmployeeSerializer,
    BasicEmployeeSerializer,
)


class EmployeViewSet(viewsets.GenericViewSet):
    queryset = Employee.objects.all()
    serializer_class = BasicEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == "create_employee":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create_employee":
            return BasicEmployeeSerializer
        return super().get_serializer_class()

    @transaction.atomic
    @action(["POST"], detail=False, url_path="create-employee")
    @extend_schema(request=CreateEmployeeSerializer, responses=BasicEmployeeSerializer)
    def create_employee(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(["GET"], detail=False, url_path="get-all-employees")
    def get_all_employees(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["GET"], detail=True, url_path="get-employee-detail")
    def get_employee_detail(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    @action(["PUT"], detail=True, url_path="update-employee-detail")
    def update_employee_detail(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.get_serializer(instance=object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(["DELETE"], detail=True, url_path="delete-employee-detail")
    def delete_employee_detail(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
