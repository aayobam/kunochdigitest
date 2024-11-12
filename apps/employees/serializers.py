from rest_framework import serializers
from apps.employees.models import Employee
from apps.users.models import CustomUser
from apps.users.serializers import BasicUserSerializer, RegisterUserSerializer
from django.db import transaction


class CreateEmployeeSerializer(RegisterUserSerializer):
    
    class Meta(RegisterUserSerializer.Meta):
        model = Employee
        fields = RegisterUserSerializer.Meta.fields + ['phone_number', 'position']
    
    def validate(self, attrs):
        return super().validate(attrs)
    
    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user_data = {key: validated_data[key] for key in ['email', 'first_name', 'last_name', 'password', "confirm_password"]}
        employee_data = {key: validated_data[key] for key in ["phone_number", "position"]}
        user = CustomUser.objects.create(**user_data) 
        Employee.objects.create(user=user, **employee_data)
        return user


class BasicEmployeeSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(read_only=True)
    class Meta:
        model = Employee
        fields = "__all__"